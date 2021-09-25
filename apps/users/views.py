from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy


def register(request):
    if not request.method == "POST":
        redirect("redirect")
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        login(request, user)
        return redirect("home")
    for code, error in form.errors.items():
        messages.error(request, error)
    return redirect("login")


class ProfileView(LoginRequiredMixin, FormMixin, DetailView):
    model = User
    template_name = "profile.html"
    form_class = UserChangeForm
    fields = ["first_name", "last_name", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.success_url = reverse_lazy("profile")

    def get_object(self):
        self.object = self.request.user._wrapped
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def get_form_kwargs(self):
        form_kwargs = super(ProfileView, self).get_form_kwargs()
        form_kwargs["instance"] = self.get_object()
        return form_kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_form(self):
        form = super().get_form()
        for name in list(form.fields.keys()):
            if name not in self.fields and name in form.fields:
                del form.fields[name]
        [
            field.widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": (_("enter") + " " + field.label.lower())
                    if hasattr(field, "label")
                    else "",
                }
            )
            for name, field in form.fields.items()
        ]
        if form.initial:
            for name, value in form.initial.items():
                if name in form.fields:
                    form.fields[name].initial = value
        return form

    def get_initial(self):
        return self.get_object().__dict__
