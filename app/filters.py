from django_filters import rest_framework as filters

from app.models import Book


class BookFilter(filters.FilterSet):

    class Meta:
        model = Book
        fields = {
            'published_date': ['lte', 'gte'],
            'title': ['icontains'],
            'author': ['icontains'],
            'lang': ['iexact'],
        }
