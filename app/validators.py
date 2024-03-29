import datetime

from django.core.exceptions import ValidationError


def validate_date(value):
    if value > datetime.date.today():
        raise ValidationError("The date cannot be from the future !")


def validate_isbn(value):
    if not value.isdigit() and not len(value) == 13:
        raise ValidationError("Enter 13 or 10 digits !")
    if not value.isdigit() and not len(value) == 10:
        raise ValidationError("Enter 13 or 10 digits !")
