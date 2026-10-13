
def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Equipment Catalogue" in response.data


def test_catalogue_page(client):
    response = client.get("/catalogue")

    assert response.status_code == 200
    assert b"Equipment Catalogue" in response.data
