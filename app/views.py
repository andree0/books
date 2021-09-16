from typing import Any

# from django.db.models import Q
from django.http import HttpRequest, HttpResponse
# from django.shortcuts import render
from django.views.generic import ListView

from app.forms import FilterBookForm
from app.models import Book


# Create your views here.
class BookList(ListView):
    model = Book

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        # form = FilterBookForm()
        # if form.is_valid:
        #     title = request.GET.get("title")
        #     author = request.GET.get("author")
        #     language = request.GET.get("language")
        #     from_date = request.GET.get("from_date")
        #     to_date = request.GET.get("to_date")
        #     queryset = Book.objects.filter(
                
        #     )
        return super().get(request, *args, **kwargs)
