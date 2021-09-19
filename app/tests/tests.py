import pytest

from app.models import Book
from app.tests.utils import fake_book_data


# Check status code 200 - method GET ---------------------------------------

@pytest.mark.django_db
def test_get_index_view(client):
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_add_book_view(client):
    response = client.get('/add-book/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_import_books_view(client):
    response = client.get('/import-books/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_edit_book_view(client, book):
    response = client.get(f'/edit-book/{book.pk}/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_delete_book_view(client, book):
    response = client.get(f'/delete-book/{book.pk}/')
    assert response.status_code == 200

# Check status code 200 - method POST ---------------------------------------


@pytest.mark.django_db
def test_add_book(client):
    book_before = Book.objects.count()
    data = fake_book_data()
    response = client.post('/add-book/', data, follow=True)
    assert response.status_code == 200
    assert Book.objects.count() == book_before + 1


@pytest.mark.django_db
def test_edit_book(client, book):
    book_before = Book.objects.count()
    data = fake_book_data()
    response = client.post(f'/edit-book/{book.pk}/', data, follow=True)
    assert response.status_code == 200
    assert Book.objects.count() == book_before


@pytest.mark.django_db
def test_delete_book(client, book):
    book_before = Book.objects.count()
    response = client.post(f'/delete-book/{book.pk}/', follow=True)
    assert response.status_code == 200
    assert Book.objects.count() == book_before - 1


@pytest.mark.django_db
def test_import_books(client):
    response = client.post('/import-books/')
    assert response.status_code == 200
