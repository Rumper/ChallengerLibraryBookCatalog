from django.shortcuts import render
from books.decorators import get_form_books
from django.contrib.auth.decorators import login_required
from books.forms import BooksFullForms, BooksInfoForms
from django.urls import reverse_lazy
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import redirect


@login_required
@get_form_books
def ajax_get_forms(request, form):
    return render(request, "books_forms.html", {"form": form})


@login_required
def ajax_create_book(request):
    if request.method != "POST":
        return HttpResponseNotAllowed("method no allowed")
    form = BooksFullForms(request.POST)
    if form.is_valid():
        instance = form.save(user=request.user)
        return JsonResponse(
            {
                "status": True,
                "success_url": reverse_lazy(
                    "books_details", kwargs={"pk": instance.pk}
                ),
            },
            status=201,
        )
    return JsonResponse({"status": False, "errors": form.errors}, status=400)


@login_required
def ajax_create_book_info(request):
    if request.method != "POST":
        return HttpResponseNotAllowed("method no allowed")
    form = BooksInfoForms(request.POST)
    if form.is_valid():
        form.save(user=request.user)
        return JsonResponse(
            {
                "status": True,
                "succes_url": reverse_lazy(
                    "books_details", kwargs={"pk": request.POST.get("book")}
                ),
            }
        )
    return JsonResponse({"status": False, "errors": form.errors}, status=400)
