import pytest
from app import *


@pytest.fixture
def client():
    
    """Fixture returning a Flask test client."""

    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_all_success(client):

    """Test for a successful request to the /all endpoint."""

    response = client.post('/all', json={
        "url": "https://example.com",
        "keywords": "example keyword"
    })
    assert response.status_code == 200  
    
    data = response.get_json()

    #Check the presence of keys in the returned response
    assert "all" in data
    assert "all with keywords" in data