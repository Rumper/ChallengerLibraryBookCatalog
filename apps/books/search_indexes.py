from haystack import indexes
from books.models import Books, BooksInfo


class BooksIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")

    def get_model(self):
        return Books

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
