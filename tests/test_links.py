from test_config import *

def test_links_success(client):
    
    """Test for a successful request to the /links endpoint."""

    response = client.post('/links', json={
        "url": "https://example.com",
        "option": "status"
    })
    assert response.status_code == 200  
    
    data = response.get_json()

    #Check the presence of keys in the returned response
    assert "" in data
