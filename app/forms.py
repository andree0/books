from django import forms


class FilterBookForm(forms.Form):
    title = forms.CharField(max_length=128, strip=True, required=False)
    author = forms.CharField(max_length=64, strip=True, required=False)
    language = forms.CharField(max_length=3, strip=True, required=False)
    from_date = forms.DateField(widget=forms.DateInput)
    to_date = forms.DateField(widget=forms.DateInput)
