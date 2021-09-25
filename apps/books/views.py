from datetime import datetime, timedelta
from django.utils.translation import gettext as _
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from books.models import Books, BooksInfo
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.http import JsonResponse
from books.forms import (
    BooksForms,
    BooksInfoForms,
    BooksFullForms,
    BooksSearchForm,
)
from django.urls import reverse_lazy
from haystack.generic_views import SearchView
from django.views.generic import TemplateView
from django.db.models import Q

# Create your views here.


class Home(LoginRequiredMixin, TemplateView):
    template_name = "index.html"
    extra_context = {
        "menu_active": "home",
    }

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        check_recented_date = datetime.now() - timedelta(days=3)
        context["last_books_added"] = Books.objects.filter(
            Q(created_date__gte=check_recented_date)
            | Q(info__created_date__gte=check_recented_date)
        )[:6]
        return context


class BooksListViews(LoginRequiredMixin, ListView):
    model = Books
    template_name = "books_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(info__isnull=False)


class BooksViews(LoginRequiredMixin, FormMixin, DetailView):
    model = Books
    template_name = "books.html"
    form_class = BooksForms

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_object(self):
        self.object = get_object_or_404(self.model, pk=self.kwargs.get("pk"))
        return self.object

    def delete(self, *args, **kwargs):
        info = get_object_or_404(BooksInfo, pk=kwargs.get("pk"))
        info.delete()
        return JsonResponse({"status": True})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form, *args, **kwargs)
        return self.form_invalid(form, *args, **kwargs)

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs["instance"] = self.get_object()
        return form_kwargs

    def form_valid(self, form, *args, **kwargs):
        form.save()
        super().form_valid(form, *args, **kwargs)
        return JsonResponse(
            {
                "status": True,
                "succes_url": reverse_lazy(
                    "books_details", kwargs={"pk": self.kwargs.get("pk")}
                ),
            },
            status=201,
        )

    def form_invalid(self, form, *ags, **kwargs):
        super().form_invalid(form, *ags, **kwargs)
        return JsonResponse(
            {"status": False, "errors": form.errors}, status=400
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["form_add_info"] = BooksInfoForms(
            initial={"book": self.kwargs.get("pk")}
        )
        return context


class BooksInfoViews(BooksViews):
    model = BooksInfo
    form_class = BooksInfoForms

    def get_object(self):
        self.object = get_object_or_404(self.model, pk=self.kwargs.get("info"))
        return self.object


class BooksSearchViews(SearchView):
    template_name = "books_search.html"
    form_class = BooksSearchForm
