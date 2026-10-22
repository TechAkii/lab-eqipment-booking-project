
# Tests whether the home page loads successfully and displays the equipment catalogue title.
def test_home_page(client):
    # Sends a GET request to the home page.
    response = client.get("/")

    # Checks that the home page returns a successful HTTP status code.
    assert response.status_code == 200

    # Checks that the equipment catalogue title appears on the page.
    assert b"Equipment Catalogue" in response.data


# Tests whether the catalogue page loads successfully and displays the equipment catalogue title.
def test_catalogue_page(client):
    # Sends a GET request to the equipment catalogue page.
    response = client.get("/catalogue")

    # Checks that the catalogue page returns a successful HTTP status code.
    assert response.status_code == 200

    # Checks that the equipment catalogue title appears on the page.
    assert b"Equipment Catalogue" in response.data