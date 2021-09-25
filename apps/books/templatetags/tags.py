from django import template
from django.utils.translation import gettext as _
from django.urls import reverse
from books.forms import BooksFullForms, BooksSearchForm


register = template.Library()


@register.inclusion_tag("menu.html", takes_context=True)
def menu(context):
    return {
        "menu": [
            {
                "name": _("Home"),
                "url": reverse("home"),
                "icon": "fa-home",
                "class": "home",
            },
            {
                "name": _("Profile"),
                "url": reverse("profile"),
                "icon": "fa-user",
                "class": "profile",
            },
            {
                "name": _("Books"),
                "url": reverse("books"),
                "icon": "fa-book",
                "class": "books",
            },
        ]
    }


@register.simple_tag(takes_context=True)
def set_form_add_books(context):
    context["form_add_books"] = BooksFullForms()


@register.simple_tag(takes_context=True)
def set_form_search_books(context):
    context["form_search_books"] = BooksSearchForm()


@register.filter(takes_context=True)
def get_elastic_object(objects):
    return [result.object for result in objects]
