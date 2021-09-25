from django.db import models
from django.utils.translation import gettext as _
from users.models import User
from books.choices import FORMAT_BOOKS_CHOICES

# Create your models here.


class AbstractModel(models.Model):
    created_date = models.DateTimeField(
        verbose_name=_("added"), auto_now=True, null=True
    )
    updated_date = models.DateTimeField(
        verbose_name=_("updated"), auto_now_add=True, null=True
    )

    class Meta:
        abstract = True


class BooksGenres(AbstractModel):
    name = models.CharField(_("name"), max_length=50)

    def __str__(self):
        return self.name


class Books(AbstractModel):
    name = models.CharField(
        verbose_name=_("name"), max_length=100, unique=True
    )
    description = models.TextField(
        verbose_name=_("description"), null=True, blank=True
    )
    genre = models.ManyToManyField(
        BooksGenres, verbose_name=_("genre"), related_name="genres"
    )

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name

    def total(self):
        return self.info.count()

    def get_genres(self):
        return ", ".join(list(self.genre.values_list("name", flat=True)))


class BooksInfo(AbstractModel):
    book = models.ForeignKey(
        Books,
        on_delete=models.CASCADE,
        verbose_name=_("book"),
        related_name="info",
    )
    editorial = models.CharField(
        verbose_name=_("editorial"), max_length=100, null=True, blank=True
    )
    publication_date = models.IntegerField(
        verbose_name=_("date of publication"), null=True
    )
    is_retired = models.BooleanField(
        verbose_name=_("is retired?"), default=False
    )
    isbn = models.CharField(verbose_name="isbn", max_length=20, unique=True)
    format = models.CharField(
        verbose_name=_("Format"), max_length=3, choices=FORMAT_BOOKS_CHOICES
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name=_("added by"),
        related_name="books_add",
        null=True,
    )

    class Meta:
        indexes = [
            models.Index(fields=["isbn", "editorial", "publication_date"]),
        ]

    def __str__(self):
        is_retired = "" if not self.is_retired else " " + _("retired")
        return f"{self.book} - {self.isbn}|{self.publication_date}{is_retired}"
