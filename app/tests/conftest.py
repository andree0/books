import pytest

from django.test import Client

from app.tests.utils import create_fake_book


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def book():
    return create_fake_book()
