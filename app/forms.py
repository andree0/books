import datetime

from django import forms
from django.forms import widgets

from app.models import Book
from app.validators import validate_date, validate_isbn

class FilterBookForm(forms.Form):
    title = forms.CharField(max_length=128, strip=True, required=False)
    author = forms.CharField(max_length=64, strip=True, required=False)
    lang = forms.CharField(max_length=3, strip=True, required=False)
    from_date = forms.DateField(widget=forms.DateInput)
    to_date = forms.DateField(widget=forms.DateInput)


class BookForm(forms.ModelForm):
    published_date = forms.DateField(
        widget = forms.SelectDateWidget(
            attrs = {
                'min': "1900-01-01",
                'max': datetime.date.today()
            },
            years=[i for i in range(1900, datetime.date.today().year + 1)]
        ),
        validators = [validate_date, ]
    )
    isbn = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                'maxlength': 13
            }
        ),
        validators = [validate_isbn, ],
        label = "ISBN (13 digits)"
    )

    class Meta:
        model = Book
        fields = (
            'title',
            'author',
            'published_date',
            'isbn',
            'page_count',
            'link',
            'lang',
        )
        widgets = {
            'lang': forms.TextInput(
                attrs={
                    'placeholder': 'for example: pl or PL',
                    'maxlength': 2,
                    }
                ),
        }
        labels = {
            'lang': 'Language',
        }
