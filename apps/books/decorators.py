from books.choices import FORM_CONVERT, MODEL_CONVERT
from django.utils.module_loading import import_string
from django.shortcuts import get_object_or_404


def get_form_books(func):
    def _decorator(request, form_type, pk):
        try:
            form_class = FORM_CONVERT[form_type]
            model_class = MODEL_CONVERT[form_type]
        except KeyError:
            raise KeyError(f"not exists key: {form_type}")
        form_class = import_string(form_class)
        model_class = import_string(model_class)
        return func(
            request, form_class(instance=get_object_or_404(model_class, pk=pk))
        )

    return _decorator
