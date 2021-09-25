from django.test import TestCase
from django.urls import reverse
from books.models import Books, BooksInfo, BooksGenres
from users.models import User

# Create your tests here.


class BooksListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="Prueba", password="contraseña")
        for idx in range(20):
            genre = BooksGenres.objects.create(name="Genre %s" % idx)
            book = Books.objects.create(
                name="Libro %s" % idx, description="Descripcion %s" % idx
            )
            book.add(genre)
            BooksInfo.objects.create(
                book=book,
                isbn=idx,
                publication_date=2001,
                editorial="Editorial %s" % idx,
                format="phy",
            )

    def test_view_url_redirect_login(self):
        resp = self.client.get(reverse("books"))
        self.assertRedirects(resp, "/accounts/login/?next=/books/")

    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(User.objects.get(pk=1))
        resp = self.client.get("/books/")
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(User.objects.get(pk=1))
        resp = self.client.get(reverse("books"))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(User.objects.get(pk=1))
        resp = self.client.get(reverse("books"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "books_list.html")


class BooksViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="Prueba", password="contraseña")
        genre = BooksGenres.objects.create(name="Genre")
        book = Books.objects.create(name="Libro", description="Descripcion")
        book.add(genre)
        BooksInfo.objects.create(
            book=book,
            isbn=1,
            publication_date=2001,
            editorial="Editorial",
            format="phy",
        )

    def test_view_url_redirect_login(self):
        resp = self.client.get(reverse("books_details", kwargs={"pk": 1}))
        self.assertEqual(resp.status_code, 302)

    def test_view_url_accessible_by_name(self):
        self.client.force_login(User.objects.get(pk=1))
        resp = self.client.get(reverse("books_details", kwargs={"pk": 1}))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.force_login(User.objects.get(pk=1))
        resp = self.client.get(reverse("books_details", kwargs={"pk": 1}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "books.html")
