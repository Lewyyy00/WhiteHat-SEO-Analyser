from test_config import *

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


def test_keywords_missing_url(client):

    """Test request without 'url' field."""

    response = client.post('/keywords', json={
        "option": "all",
        "analysingobject": "content"
    })

    assert response.status_code == 400  # Response code for error
    data = response.get_json()

    assert "error" in data  # Check if 'error' key is present
    assert "Missing parameters: url" in data["error"]  # Match the message

def test_keywords_missing_analysingobject(client):

    """Test request without 'analysingobject' field."""

    response = client.post('/keywords', json={
        "url": "https://example.com",
        "option": "all"
    })

    assert response.status_code == 400  
    data = response.get_json()

    assert "error" in data  
    assert "Missing parameters: analysingobject" in data["error"]  

def test_keywords_missing_option(client):

    """Test request without 'option' field."""

    response = client.post('/keywords', json={
        "url": "https://example.com",
        "analysingobject": "content"
    })

    assert response.status_code == 400  
    data = response.get_json()

    assert "error" in data  
    assert "Missing parameters: option" in data["error"]  