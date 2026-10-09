def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Lab Equipment Booking System" in response.data