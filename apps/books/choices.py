from django.utils.translation import gettext as _

FORMAT_DIGITAL = "dig"
FORMAT_PHYSICAL = "phy"

FORMAT_BOOKS_CHOICES = [
    (FORMAT_PHYSICAL, _("physical")),
    (FORMAT_DIGITAL, _("digital")),
]


FORM_CONVERT = {
    "books": "books.forms.BooksForms",
    "books_info": "books.forms.BooksInfoForms",
}


MODEL_CONVERT = {
    "books": "books.models.Books",
    "books_info": "books.models.BooksInfo",
}
