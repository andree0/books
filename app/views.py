from typing import Any, Tuple

# from django.db.models import Q
from django.http import HttpRequest, HttpResponse
# from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, UpdateView

from app.forms import BookForm, FilterBookForm
from app.models import Book


# Create your views here.
class BookListView(ListView):
    model = Book

    # def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
    #     form = FilterBookForm()
    #     if form.is_valid:
    #         title = request.GET.get("title")
    #         author = request.GET.get("author")
    #         lang = request.GET.get("lang")
    #         from_date = request.GET.get("from_date")
    #         to_date = request.GET.get("to_date")
    #         queryset = Book.objects.filter(
    #             title__icontains = title,
    #             author__icontains = author,
    #             lang__iexact = lang,
    #             published_date__range = (from_date, to_date)
    #         )
    #     return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        super().get_queryset()
        queryset = self.model.objects.all()
        filter_fields: Tuple = (
            'title__icontains',
            'author__icontains',
            'lang__iexact',
            'published_date__gte',
            'published_date__lte',
            )
        dict_filters = {}
        for filter in filter_fields:
            if value := self.request.GET.get(filter):
                dict_filters[filter] = value
        if dict_filters:
            queryset = self.model.objects.filter(**dict_filters)
        return queryset


class AddBookView(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy("book_list")


class EditBookView(UpdateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy("book_list")


class DeleteBookView(DeleteView):
    model = Book
    success_url = reverse_lazy("book_list")
