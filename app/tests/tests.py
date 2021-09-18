import pytest

from app.models import Book


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
