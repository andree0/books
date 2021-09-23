import datetime
from bootstrap_datepicker_plus import DatePickerInput

from django import forms

from app.models import Book
from app.validators import validate_date, validate_isbn


class FilterBookForm(forms.Form):
    title__icontains = forms.CharField(
        max_length=128,
        strip=True,
        required=False,
        label="Title"
        )
    author__icontains = forms.CharField(
        max_length=64,
        strip=True,
        required=False,
        label="Author"
        )
    lang__iexact = forms.CharField(
        max_length=2,
        strip=True,
        required=False,
        label="Language"
        )
    published_date__gte = forms.DateField(
        widget=DatePickerInput(
            options={
                "format": "YYYY-MM-DD",
                "showClose": True,
                "showClear": True,
                "showTodayButton": True,
                "maxDate": str(datetime.date.today()),
                "useCurrent": False,
            }
        ),
        label="From",
        required=False
        )
    published_date__lte = forms.DateField(
        widget=DatePickerInput(
            options={
                "format": "YYYY-MM-DD",
                "showClose": True,
                "showClear": True,
                "showTodayButton": True,
                "maxDate": str(datetime.date.today()),
                "useCurrent": False,
            }
        ),
        label="To",
        required=False
        )


class BookForm(forms.ModelForm):
    published_date = forms.DateField(
        widget=DatePickerInput(
            options={
                "format": "YYYY-MM-DD",
                "showClose": True,
                "showClear": True,
                "showTodayButton": True,
                "maxDate": str(datetime.date.today()),
                "useCurrent": False,
            }
        ),
        validators=[validate_date, ]
    )
    isbn = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'maxlength': 13
            }
        ),
        validators=[validate_isbn, ],
        label="ISBN (13 or 10 digits)"
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


class ImportBookForm(forms.Form):
    TERMS = (
        ('', '', ),
        ('intitle', 'intitle', ),
        ('inauthor', 'inauthor', ),
        ('isbn', 'isbn', )
    )
    key_word = forms.CharField(max_length=128, strip=True)
    term = forms.ChoiceField(
        choices=TERMS,
        required=False,
        label="Term (optional)",
        )
