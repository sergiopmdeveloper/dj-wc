import pytest
from django.test import Client, RequestFactory


@pytest.fixture
def rf() -> RequestFactory:
    """
    RequestFactory fixture
    """

    return RequestFactory()


@pytest.fixture
def client() -> Client:
    """
    Client fixture
    """

    return Client()
