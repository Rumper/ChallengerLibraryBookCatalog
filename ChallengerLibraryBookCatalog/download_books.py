import requests
import random
from bs4 import BeautifulSoup
from books.models import Books, BooksInfo, BooksGenres


http_books = "https://es.wikipedia.org/wiki/"
list_books = [
    "El_Señor_de_los_Anillos",
    "Reina_Roja_(novela)",
    "Contrato_con_Dios_(novela_de_Juan_Gómez-Jurado)",
    "Hombres_buenos",
]


def download_books():
    for bookk in list_books:
        res = requests.get(http_books + bookk)
        soup = BeautifulSoup(res.text, "html.parser")
        title = soup.title.string.replace(
            " - Wikipedia, la enciclopedia libre", ""
        )
        info_box = soup.find("table", {"class": "infobox"})
        ths = info_box.find_all("th")
        generos = []
        editorial = None
        for th in ths:
            if "cabecera" in th.attrs and "libro" in th.attrs:
                title = th.text.replace("\n", "")
                continue
            if th.text == "Subgénero":
                for a in th.parent.find_all("a"):
                    generos.append(a.text.replace("\n", ""))
                continue
            if th.text == "Editorial":
                editorial == th.parent.td.text.replace("\n", "")
                continue
        p = soup.find_all("p")
        description = p[0].text + "\n" + p[1].text
        isbn = int(random.random() * 1000000000000)
        gens = [
            BooksGenres.objects.get_or_create(name=genero.capitalize())[0]
            for genero in generos
            if genero
        ]
        book = Books.objects.get_or_create(
            name=title, description=description
        )[0]
        book.save()
        book.genre.add(*list(gens))
        BooksInfo.objects.get_or_create(
            book=book,
            isbn=isbn,
            publication_date=random.randrange(1900, 2021),
            editorial=editorial,
            format="phy",
        )
