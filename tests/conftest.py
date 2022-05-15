import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.book import Book 


@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_books(app):
    # Arrange
    space_book = Book(title="Dune",
                      description="anarchist space scifi")
    earth_book = Book(title="Parable of the Sower",
                         description="post-apoalyptic scifi")

    db.session.add_all([space_book, earth_book])
    db.session.commit() 
    