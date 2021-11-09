from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = sqlite3.connect("the_books_wishlist.db", check_same_thread=False)
cursor = db.cursor()

all_books = []

# for row in cursor.execute("SELECT * FROM books"):
#     new_book = {
#         "title": row[0],
#         "author": row[1],
#         "rate": row[2]
#     }
#     all_books.append(new_book)


@app.route('/')
def home():
    # cursor.execute("CREATE TABLE my_books (title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")

    books_table =  cursor.execute("SELECT * FROM my_books")
    return render_template("index.html", books = books_table)


@app.route("/add", methods = ['GET', 'POST'])
def add():
    if request.method == 'POST':
        cursor.execute(f"INSERT INTO my_books VALUES(?,?,?)",
        (request.form['title'], request.form['author'], request.form['rate']))
        db.commit()

        return redirect(url_for('home'))
    return render_template("add.html")

@app.route('/delete/<title>')
def delete_item(title):
    print(title)
    cursor.execute("DELETE FROM my_books WHERE title=?",(title,))
    db.commit()
    return redirect(url_for('home'))

@app.route('/<book_title>/<current_rate>', methods = ['GET', 'POST'])
def edit_rating(book_title, current_rate):
    if request.method == 'POST':
        cursor.execute("UPDATE my_books SET rating = ? WHERE title = ?", (request.form['new_rating'], book_title))
        db.commit()

        return redirect(url_for('home'))

    # cursor.execute("SELECT * FROM my_books WHERE title = ?",(book_title,))
    # content = cursor.fetchall()
    # print(content)

    return render_template("edit_data.html", book_title=book_title, book_rating=current_rate)


if __name__ == "__main__":
    app.run(debug=True)

