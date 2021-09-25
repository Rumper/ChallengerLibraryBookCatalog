from django.contrib import admin

# Register your models here.
from .models import Books, BooksInfo, BooksGenres


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    pass


@admin.register(BooksInfo)
class BooksInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(BooksGenres)
class BooksGenresAdmin(admin.ModelAdmin):
    pass
