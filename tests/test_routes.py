def test_get_all_books_with_no_records(client):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_all_books(client, two_books):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

   
    assert response.status_code == 200
    assert response_body == [{
        "id": 1,
        "title": "Dune",
        "description": "anarchist space scifi"
    },
    
    { "id": 2,
        "title": "Parable of the Sower",
        "description": "post-apoalyptic scifi"

    }]

def test_get_one_book(client, two_books):
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Dune",
        "description": "anarchist space scifi"
    }

def test_get_book_no_db(client):
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {'message': 'book with id #1 not found'}


def test_create_book(client):
    # Act
    response = client.post("/books", json={
        "title": "The Baron in the Trees",
        "description": "A ridiculous comedic fiction"
    })
    response_body = response.get_json()

    assert response_body == ["Book The Baron in the Trees successfully created",201]