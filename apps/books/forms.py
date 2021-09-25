from django import forms
from books.models import Books, BooksInfo
from django.forms import formset_factory
from django.template.loader import render_to_string
from django.db import transaction
from haystack.forms import SearchForm
from django.utils.translation import gettext as _
from books.widgets import SlimSelect


class BooksForms(forms.ModelForm):
    class Meta:
        model = Books
        fields = "__all__"
        widgets = {"genre": SlimSelect()}


class BooksInfoForms(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["format"].widget.attrs["class"] = "form-control"

    class Meta:
        model = BooksInfo
        fields = "__all__"
        exclude = ["is_retired", "user"]
        widgets = {"book": forms.HiddenInput()}

    def save(self, *args, **kwargs):
        if kwargs.get("book"):
            self.instance.book = kwargs["book"]
        if kwargs.get("user"):
            self.instance.user = kwargs["user"]
        return self.instance.save()


class BooksBaseFormSet(forms.formsets.BaseFormSet):
    def as_div(self):
        "Return this formset rendered as HTML <div>."
        return render_to_string("books_formset.html", {"forms": self})

    def save(self, book, user):
        for form in self.forms:
            form.save(book=book, user=user)


class BooksInfoFormsByFormset(BooksInfoForms):
    class Meta(BooksInfoForms.Meta):
        exclude = BooksInfoForms.Meta.exclude + ["book"]


class BooksFullForms(BooksForms):
    prefix = "full"
    info = formset_factory(
        BooksInfoFormsByFormset, formset=BooksBaseFormSet, extra=0, min_num=1
    )

    def is_valid(self):
        self.formset = self.info(self.data)
        is_valid = super().is_valid() and self.formset.is_valid()
        if not is_valid and self.formset.errors:
            self.errors.update({"formset": self.formset.errors})
        return is_valid

    def save(self, user=None, *args, **kwargs):
        with transaction.atomic():
            self.instance.save()
            self.instance.genre.add(*self.cleaned_data["genre"])
            self.formset.save(book=self.instance, user=user)
        return self.instance


class BooksSearchForm(SearchForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["q"].label = ""
        self.fields["q"].widget.attrs.update(
            {
                "placeholder": _("Enter an press by search"),
                "class": "form-control",
            }
        )
