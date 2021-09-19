# other way
import requests
from django_filters import rest_framework as filters
from rest_framework.generics import ListAPIView
from typing import Dict, Tuple

# default django
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.edit import DeleteView, FormView, UpdateView

# my app
from app.filters import BookFilter
from app.forms import BookForm, FilterBookForm, ImportBookForm
from app.models import Book
from app.serializers import BookSerializer
from project.settings import APP_PAGINATE_BY


class BookListView(ListView):
    model = Book
    paginate_by = APP_PAGINATE_BY
    ordering = ("-published_date", "title", )

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
        context["querystring"] = "&".join(
            [i for i in all_querystring if "page" not in i])
        context["form"] = FilterBookForm(initial=self.request.GET)
        return context

    def get_queryset(self):
        super().get_queryset()
        queryset = self.model.objects.all().order_by(*self.ordering)
        dict_filters = {}
        for filter in self.FILTERS:
            if value := self.request.GET.get(filter):
                dict_filters[filter] = value
        if dict_filters:
            try:
                queryset = self.model.objects.filter(
                    **dict_filters).order_by(*self.ordering)
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
    template_name = "app/book_confirm_delete.html"
    success_url = reverse_lazy("book_list")
    context = {}

    def get(self, request, pk, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=pk)
        self.context["obj"] = obj
        return render(request, self.template_name, self.context)


class ImportBookView(FormView):
    form_class = ImportBookForm
    template_name = "app/book_form.html"
    success_url = reverse_lazy("book_list")

    def load_books_data(self, key_word: str, term=None) -> Dict:
        """Download data books from api google"""
        url: str = "https://www.googleapis.com/books/v1/volumes"
        params: Dict = {
            "q": f"{key_word}+{term}" if term else f"{key_word}",
            "printType": "books"
        }
        return requests.get(url=url, params=params).json()

    def find_required_book_data(self, book: Dict) -> Dict:
        """Find required book data and validate it."""
        info = book.get("volumeInfo", {})
        data: Dict = {
            'title': info.get("title", ""),
            'page_count': info.get("pageCount", 1),
            'link': info.get("imageLinks", {}).get("thumbnail", "no link"),
            'lang': info.get("language", ""),
        }

        # validate author
        if not info.get("authors"):
            data["author"] = None
        else:
            data["author"] = ", ".join(info.get("authors"))

        # validate published date
        if len(date := info.get("publishedDate", "")) == 10:
            data["published_date"] = date
        elif len(date := info.get("publishedDate", "")) == 4:
            data["published_date"] = date + "-01-01"
        elif len(date := info.get("publishedDate", "")) == 7:
            data["published_date"] = date + "-01"
        else:
            data["published_date"] = None

        # validate isbn
        if not info.get("industryIdentifiers"):
            data["isbn"] = None
        else:
            for type in info.get("industryIdentifiers"):
                if type.get("type", "") == "ISBN_13":
                    data["isbn"] = type.get("identifier")
                elif type.get("type", "") == "ISBN_10":
                    data["isbn"] = type.get("identifier")
                else:
                    data["isbn"] = None

        # skip book with invalid data
        for val in data.values():
            if not val:
                return {}
        return data

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid:
            key_word = request.POST.get("key_word")
            term = request.POST.get("term")
            books_data = self.load_books_data(key_word, term)
            old_count_books = Book.objects.count()
            for book in books_data.get("items", []):
                if data := self.find_required_book_data(book):
                    Book.objects.get_or_create(**data)
            count_added_books = Book.objects.count() - old_count_books
            messages.success(request, f"Added {count_added_books} books.")
        return super().post(request, *args, **kwargs)


# API View
class BookAPIView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = BookFilter
