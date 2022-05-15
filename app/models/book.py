from app import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    author_description = db.column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship("Author", back_populates='books')
