import pytest
from app import *

@pytest.fixture
def client():
    
    """Fixture returning a Flask test client."""

    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client