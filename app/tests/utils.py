from faker import Faker
from random import randint


from app.models import Book

fake = Faker("en-US")


def fake_book_data():
    """Generate a dict of book data"""
    nr = randint(1, 4)
    return {
        'title': fake.text(max_nb_chars=20),
        'author': fake.first_name() + fake.last_name(),
        'published_date': fake.date(),
        'isbn': fake.isbn13(separator=""),
        'page_count': fake.random_number(digits=nr),
        'link': fake.url(),
        'lang': fake.language_code(),
    }


def create_fake_book():
    return Book.objects.create(**fake_book_data())
