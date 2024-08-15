import pytest
from django.test import RequestFactory


@pytest.fixture
def rf() -> RequestFactory:
    """
    RequestFactory fixture
    """

    return RequestFactory()
