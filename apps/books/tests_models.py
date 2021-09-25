from django.test import TestCase
from books.models import Books, BooksInfo, BooksGenres


# Create your tests here.
class BookGenreTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        BooksGenres.objects.create(name="Comedia")

    def setUp(self):
        pass

    def test_name(self):
        genre = BooksGenres.objects.get(pk=1)
        self.assertEquals(genre.name, "Comedia")


class BooksInfoTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Books.objects.create(
            name="El Hobbit", description="Mundo del señor de los anillos"
        )
        BooksInfo.objects.create(
            book=Books.objects.get(pk=1),
            isbn="9780044403371",
            publication_date=1973,
            format="phy",
            editorial="Editorial",
        )

    def setUp(self):
        pass

    def test_isbn(self):
        info = BooksInfo.objects.get(pk=1)
        self.assertEquals(info.isbn, "9780044403371")

    def test_publication_date(self):
        info = BooksInfo.objects.get(pk=1)
        self.assertEquals(info.publication_date, 1973)

    def test_editorial(self):
        info = BooksInfo.objects.get(pk=1)
        self.assertEquals(info.editorial, "Editorial")

    def test_format(self):
        info = BooksInfo.objects.get(pk=1)
        self.assertEquals(info.format, "phy")

    def test_book(self):
        info = BooksInfo.objects.get(pk=1)
        book = Books.objects.get(pk=1)
        self.assertEquals(book.info.get(pk=1), info)


class BookTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Books.objects.create(
            name="El Hobbit", description="Mundo del señor de los anillos"
        )

    def test_name(self):
        book = Books.objects.get(pk=1)
        self.assertEquals(book.name, "El Hobbit")

    def test_description(self):
        book = Books.objects.get(pk=1)
        self.assertEquals(book.description, "Mundo del señor de los anillos")

    def test_genre(self):
        book = Books.objects.get(pk=1)
        genre = BooksGenres.objects.create(name="Comedia")
        book.genre.add(genre)
        self.assertEquals(book.genre.get(pk=1), genre)
