from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Koneksi ke MongoDB dengan URL koneksi yang Anda berikan
client = MongoClient('mongodb+srv://test:sparta@cluster0.hzfbzhd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.book_collection
books = db.books

@app.route('/')
def index():
    all_books = books.find()
    return render_template('index.html', books=all_books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        books.insert_one({'title': title, 'author': author, 'year': year})
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/edit/<book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = books.find_one({'_id': ObjectId(book_id)})
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = request.form['year']
        books.update_one({'_id': ObjectId(book_id)}, {'$set': {'title': title, 'author': author, 'year': year}})
        return redirect(url_for('index'))
    return render_template('edit_book.html', book=book)

@app.route('/delete/<book_id>')
def delete_book(book_id):
    books.delete_one({'_id': ObjectId(book_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
