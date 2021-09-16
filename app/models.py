from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=64)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13)
    page_count = models.PositiveIntegerField()
    link = models.CharField(max_length=255)
    lang = models.CharField(max_length=3)
