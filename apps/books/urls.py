"""ChallengerLibraryBookCatalog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from importlib import import_module
from django.contrib import admin
from django.urls import path
from django.conf import settings
from books.views import (
    Home,
    BooksListViews,
    BooksViews,
    BooksInfoViews,
    BooksSearchViews,
)
from books.ajax import ajax_get_forms, ajax_create_book, ajax_create_book_info


urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("books/", BooksListViews.as_view(), name="books"),
    path("books/add", ajax_create_book, name="books_add"),
    path("books/info/add", ajax_create_book_info, name="books_add_info"),
    path("books/<int:pk>", BooksViews.as_view(), name="books_details"),
    path("books/<int:pk>/edit/", BooksViews.as_view(), name="books_edit"),
    path(
        "books/<int:pk>/edit_info/<int:info>",
        BooksInfoViews.as_view(),
        name="books_info_edit",
    ),
    path("books/delete/<int:pk>", BooksViews.as_view(), name="books_delete"),
    path(
        "books/ajax_get_forms/<str:form_type>/<int:pk>",
        ajax_get_forms,
        name="ajax_get_forms",
    ),
    path("books/buscar", BooksSearchViews.as_view(), name="books_search"),
]
