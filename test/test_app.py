# test/test_app.py


from fastapi import testclient

@testclient
def test_read_main(client: testclient.TestClient) -> None:
    response = client.get("/heartcheck")
    assert response.status_code == 200
    
