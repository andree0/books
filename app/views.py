import datetime
import requests
from django_filters import rest_framework as filters
from rest_framework.generics import ListAPIView
from typing import Dict, Tuple

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, FormView, UpdateView

from app.filters import BookFilter
from app.forms import BookForm, FilterBookForm, ImportBookForm
from app.models import Book
from app.serializers import BookSerializer


PAGINATE_BY = 10


class BookListView(ListView):
    model = Book
    paginate_by = PAGINATE_BY
    FILTERS: Tuple = (
        'title__icontains',
        'author__icontains',
        'lang__iexact',
        'published_date__gte',
        'published_date__lte',
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_querystring = f"{self.request.GET.urlencode()}".split("&")
        context["querystring"] = "&".join([ i for i in all_querystring if not "page" in i])
        context["form"] = FilterBookForm(initial=self.request.GET)
        return context

    def get_queryset(self):
        super().get_queryset()
        queryset = self.model.objects.all()
        dict_filters = {}
        for filter in self.FILTERS:
            if value := self.request.GET.get(filter):
                dict_filters[filter] = value
        if dict_filters:
            try:
                queryset = self.model.objects.filter(**dict_filters)
            except ValidationError:
                messages.error(self.request, "Bad date format.")
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


class ImportBookView(FormView):
    form_class = ImportBookForm
    template_name = "app/book_form.html"
    success_url = reverse_lazy("book_list")

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid:
            key_word = request.POST.get("key_word")
            term = request.POST.get("term")
            url: str = f"https://www.googleapis.com/books/v1/volumes"
            params = {
                "q": f"{key_word}+{term}",
                "printType": "books"
            }
            response = requests.get(url=url, params=params).json()
            for book in response.get("items"):
                info = book.get("volumeInfo", {})
                data: Dict = {
                    'title': info.get("title", ""),
                    'author': str(info.get("authors", ""))[2:-2],
                    'isbn': info.get(
                        "industryIdentifiers",
                        [{'identifier': '0000000000000'}])[0].get("identifier"),
                    'page_count': info.get("pageCount", 1),
                    'link': info.get("imageLinks", {}).get("thumbnail", ""),
                    'lang': info.get("language", ""),
                }
                if len(date := info.get("publishedDate", "")) == 10:
                    data["published_date"] = date
                elif len(date := info.get("publishedDate", "")) == 4:
                    data["published_date"] = date + "-01-01"
                elif len(date := info.get("publishedDate", "")) == 7:
                    data["published_date"] = date + "-01"
                else:
                    data["published_date"] = str(datetime.date.today())
                Book.objects.create(**data)

        return super().post(request, *args, **kwargs)


# API View
class BookAPIView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = BookFilter
