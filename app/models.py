from django.db import models


class Book(models.Model):
    title = models.CharField()
    author = models.CharField()
    publish_date = models.DateField()
    isbn = models.PositiveIntegerField()
    pages = models.PositiveIntegerField()
    link = models.CharField()
    lang = models.CharField()
