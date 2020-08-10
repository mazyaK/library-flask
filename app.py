from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:mazyakidze652@localhost:5432/library"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    books = db.relationship('Book', backref='category', lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Category {self.name}"


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    date_of_birth = db.Column(db.Date())
    books = db.relationship('Book', backref='author', lazy=True)

    def __init__(self, first_name, last_name, date_of_birth):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth

    def __repr__(self):
        return f"Author: {self.first_name} {self.last_name}"


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    content = db.Column(db.Text())
    released_at = db.Column(db.Date())

    def __init__(self, name, category_id, author_id, content, released_at):
        self.name = name
        self.category_id = category_id
        self.author_id = author_id
        self.content = content
        self.released_at = released_at

    def __repr__(self):
        return f"Book {self.name}"


@app.route('/authors', methods=['POST', 'GET'])
def handle_authors():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_author = Author(first_name=data['first_name'],
                                last_name=data['last_name'],
                                date_of_birth=data['date_of_birth'])
            db.session.add(new_author)
            db.session.commit()
            return {"message": f"Author {new_author.first_name} {new_author.last_name} has been created successfully."}
        else:
            return {"error": f"The request payload is not in JSON format."}

    elif request.method == "GET":
        authors = Author.query.all()
        results = [
            {
                "id": author.id,
                "first_name": author.first_name,
                "last_name": author.last_name,
                "date_of_birth": author.date_of_birth,
            } for author in authors
        ]

        return {"count": len(results), "authors": results}


@app.route('/authors/<author_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_author(author_id):
    author = Author.query.get_or_404(author_id)

    if request.method == 'GET':
        response = {
            "first_name": author.first_name,
            "last_name": author.last_name,
            "date_of_birth": author.date_of_birth,
        }
        return {"message": "success", "author": response}

    elif request.method == 'PUT':
        data = request.get_json()
        author.first_name = data['first_name']
        author.last_name = data['last_name']
        author.date_of_birth = data['date_of_birth']
        db.session.add(author)
        db.session.commmmit()
        return {"message": f"Author successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(author)
        db.session.commit()
        return {"message": f"Author {author.first_name} {author.last_name} successfully deleted"}


@app.route('/categories', methods=['POST', 'GET'])
def handle_categories():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_category = Category(name=data['name'])
            db.session.add(new_category)
            db.session.commit()
            return {"message": f"Category {new_category.name} has been created successfully."}
        else:
            return {"error": f"The request payload is not in JSON format."}

    elif request.method == 'GET':
        categories = Category.query.all()
        results = [
            {
                "id": category.id,
                "name": category.name
            } for category in categories
        ]
        return {"count": len(results), "categories": results}


@app.route('/categories/<category_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_category(category_id):
    category = Category.query.get_or_404(category_id)

    if request.method == "GET":
        response = {
            "name": category.name
        }
        return {"message": "success", "category": response}

    elif request.method == 'PUT':
        data = request.get_json()
        category.first_name = data['name']
        db.session.add(category)
        db.session.commmmit()
        return {"message": f"Category successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(category)
        db.session.commit()
        return {"message": f"Author {category.name} successfully deleted"}


@app.route('/books', methods=['POST', 'GET'])
def handle_books():
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            new_book = Book(name=data['name'],
                            category_id=data['category_id'],
                            author_id=data['author_id'],
                            content=data['content'],
                            released_at=data['released_at'], )
            db.session.add(new_book)
            db.session.commit()
            return {"message": f"Category {new_book.name} has been created successfully."}
        else:
            return {"error": f"The request payload is not in JSON format."}

    elif request.method == 'GET':
        books = Book.query.all()
        results = [
            {
                "id": book.id,
                "name": book.name,
                "category_id": book.category_id,
                "author_id": book.author_id,
                "content": book.content,
                "released_at": book.released_at,
            } for book in books
        ]
        return {"count": len(results), "books": results}


@app.route('/books/<book_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_book(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == 'GET':
        response = {
            "name": book.name,
            "category_id": book.category_id,
            "author_id": book.author_id,
            "content": book.content,
            "released_at": book.released_at,
        }
        return {"message": "success", "book": response}

    elif request.method == 'PUT':
        data = request.get_json()
        book.name = data['name']
        book.category_id = data['category_id']
        book.author_id = data['author_id']
        book.content = data['content']
        book.released_at = data['released_at']
        db.session.add(book)
        db.session.commmmit()
        return {"message": f"Book successfully updated"}

    elif request.method == 'DELETE':
        db.session.delete(book)
        db.session.commit()
        return {"message": f"Book {book.name} successfully deleted"}


if __name__ == '__main__':
    app.run(debug=True)
