from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

books = [
    {'id': 1, 'title': '1984', 'author': 'George Orwell'},
    {'id': 2, 'title': 'To Kill a Mockingbird', 'author': 'Harper Lee'}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify({'books': books})

@app.route('/books', methods=['POST'])
def add_book():
    new_book = request.get_json()
    new_book['id'] = (books[-1]['id'] + 1) if books else 1
    books.append(new_book)
    return jsonify(new_book), 201

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = next((b for b in books if b['id'] == id), None)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    data = request.get_json()
    book.update(data)
    return jsonify(book)

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    global books
    book = next((b for b in books if b['id'] == id), None)
    if not book:
        return jsonify({'message': 'Book not found'}), 404
    books = [b for b in books if b['id'] != id]
    return jsonify({'message': 'Book deleted'}), 200

@app.route('/books/search')
def search_books():
    title = request.args.get('title', '').lower()
    results = [book for book in books if title in book['title'].lower()]
    return jsonify({'results': results}) if results else (jsonify({'message': 'No books found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
