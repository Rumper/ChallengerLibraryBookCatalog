from django.test import TestCase
from books.models import Books, BooksInfo
from books.forms import BooksForms, BooksInfoForms


class BooksFormsTest(TestCase):
    model_class = Books
    form_class = BooksForms
    fields = "__all__"

    def test_booksforms_model(self):
        form = self.form_class()
        self.assertTrue(form.Meta.model, self.model_class)

    def test_booksforms_fields(self):
        form = self.form_class()
        self.assertTrue(form.Meta.fields, self.fields)


class BooksInfoFormsTest(BooksFormsTest):
    model_class = BooksInfo
    form_class = BooksInfoForms
