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
    assert "headings" in data[0]
    assert "title" in data[0]

def test_choose_success(client):

    """Test for a successful request to the /choose endpoint."""
    
    #headings is not accepted
    options = ['title', 'metadescription', 'content', 'altcontent', 'urlcontent']
    for option in options:
        print(option)
        response = client.post('/choose', json={
            "url": "https://example.com",
            "option": f'{option}'
        })
        assert response.status_code == 200  

        data = response.get_json()

        #Check the presence of keys in the returned response
        assert isinstance(data, list)
        assert len(data) == 2
        assert "Missing value" in data[0]
        assert "Multiple values" in data[0]
        assert "Number of characters" in data[0]
        assert "Text" in data[0]
        #assert "kewords density" in data[1]
        #assert "keywords" in data[1]