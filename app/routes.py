from app import db
from app.models.book import Book
from app.models.author import Author 
from flask import Blueprint, jsonify, make_response, request, abort
# class Book:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description

# books = [
#     Book(1, "Fictional Book", "A fantasy novel set in an imaginary world."),
#     Book(2, "Wheel of Time", "A fantasy novel set in an imaginary world."),
#     Book(3, "Fictional Book Title", "A fantasy novel set in an imaginary world.")
# ]

books_bp = Blueprint("books_bp", __name__, url_prefix="/books")
authors_bp = Blueprint("authors_bp", __name__, url_prefix="/authors")



#get all books 
#filter books by title: %20 for space 
# as URL for title: /books?title=Not%20a%20book

@authors_bp.route("", methods=["GET"])
def get_all_authors():
    name_query = request.args.get("name")
    if name_query:
        authors = Book.query.filter_by(name=name_query)
        ## A WAY TO RETURN A RESPONSE IF THE TITLE DOESN"T EXIST? 
    else:
        authors = Author.query.all()

        authors_response = []
        for author in authors:
            authors_response.append(
                {
                    "name": author.name

                }

            )

        return jsonify(authors_response)

@authors_bp.route("", methods=["POST"])
def create_author(): 
    request_body = request.get_json()
    ## IF NAME NOT IN REQUEST_BODY THROW ERROR MESSAGE
    new_author = Author(name = request_body["name"],)

    db.session.add(new_author)
    db.session.commit()

    return make_response(jsonify(f"Author {new_author.name} successfully created"), 201)


@books_bp.route("", methods=["GET"])
def read_all_books():
    title_query = request.args.get("title")
    if title_query:
        books = Book.query.filter_by(title=title_query)
        ## A WAY TO RETURN A RESPONSE IF THE TITLE DOESN"T EXIST? 
    else:
        books = Book.query.all()
  

    books_response = []
    for book in books:
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })

    return jsonify(books_response)

@books_bp.route("", methods=["POST"])    
def create_book():

    request_body = request.get_json()
    new_book = Book(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} successfully created", 201))


# @books_bp.route("/<book_id>", methods=["GET", "PUT", "DELETE"])
# def handle_book(book_id):
#     book = Book.query.get(book_id)
#     if book == None:
#         return Response("", status=404)
#     # ... rest of our route

def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        abort(make_response({"message":f"book {book_id} invalid"}, 400))

    book = Book.query.get(book_id)

    if not book:
        abort(make_response({"message":f"book with id #{book_id} not found"}, 404))

    return book

@books_bp.route("/<book_id>", methods=["GET"])
def read_one_book(book_id):
    book = validate_book(book_id)
    return {
            "id": book.id,
            "title": book.title,
            "description": book.description
        }

#UPDATE A BOOK
@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    if request.method == "PUT":
        book = validate_book(book_id)

        request_body = request.get_json()

        book.title = request_body["title"]
        book.description = request_body["description"]

        db.session.commit()

        return make_response(jsonify(f"Book #{book.id} successfully updated"))

        

@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_book(book_id)

    db.session.delete(book)
    db.session.commit()

    return make_response(jsonify(f"Book #{book.id} successfully deleted"))



