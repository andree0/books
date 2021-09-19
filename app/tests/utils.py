from faker import Faker

from app.models import Book

fake = Faker("en-US")


def fake_book_data():
    """Generate a dict of book data"""
    return {
        'title': fake.text(max_nb_chars=20),
        'author': fake.name(),
        'published_date': fake.date_between(),  # default start '-30y' and end 'today'
        'isbn': fake.isbn13(separator=""),
        'page_count': fake.random_int(min=1, max=800),
        'link': fake.url(schemes=["http"]),
        'lang': fake.language_code(),
    }


def create_fake_book():
    return Book.objects.create(**fake_book_data())
