import pytest
from app import *


@pytest.fixture
def client():
    
    """Fixture returning a Flask test client."""

    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_keywords_success(client):

    """Test for a successful request to the /keywords endpoint."""

    response = client.post('/keywords', json={
        "url": "https://example.com",
        "option": "all",
        "analysingobject": "title",
        "querytext": "example query",
        "n": 2
    })
    assert response.status_code == 200  
    
    data = response.get_json()

    #Check the presence of keys in the returned response
    assert "Analysing object" in data
    assert "Elements" in data
    assert "Keyword_density" in data
    assert "Keywords in paragraphs" in data