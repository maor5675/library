from multiprocessing.sharedctypes import Value
import os
import sqlite3
from flask import Blueprint, Flask, g, render_template, request, redirect, session, url_for
from app.login import login_required, name, login
from app.upload import upload_file
import datetime

con = sqlite3.connect("books.db", check_same_thread=False)
con.row_factory = sqlite3.Row
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS books (bookid INTEGER  PRIMARY KEY AUTOINCREMENT ,title, author, genre, year , Quantity , filename)")
cur.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER  PRIMARY KEY AUTOINCREMENT , username UNIQUE, password, email,address,phonenumber)")
cur.execute("CREATE TABLE IF NOT EXISTS loans (loanid INTEGER  PRIMARY KEY AUTOINCREMENT , username int FOREIGN KEY REFERENCES user(id) , bookid int FOREIGN KEY REFERENCES books(bookid), takendate ,returndate)")
cur.execute("CREATE TABLE IF NOT EXISTS purchasebooks (buyid INTEGER  PRIMARY KEY AUTOINCREMENT , username,price)")
con.commit()

# def change_table():
#     cur.execute("ALTER TABLE books ADD filename ")
#     con.commit()
# change_table()

books_bp = Blueprint('books', __name__, url_prefix='/books')

@books_bp.route("/")
@login_required
def books():
    print(session.get('username'))
    # session['username'] = 'admin'
    print(request.cookies)
    # session.pop('username', None)
    result = cur.execute("SELECT *,rowid from books")    
    new_result = []
    for book in result:
        new_result.append({
            'title' : book[1],
            'author': book[2],
            'genre': book[3],
            'year': book[4],
            "Quantity": book[5],
            'filename': f'uploads/{book[6]}',
            'id': book[0]
        })
    return render_template("books.html", books=new_result)


@books_bp.route("/searchbook")
@login_required
def searchbook():
    search = request.args.get('search')
    result = cur.execute(f"SELECT *,rowid from books WHERE title LIKE '%{search}%'")    
    new_result = []
    for book in result:
        new_result.append({
            'title' : book[1],
            'author': book[2],
            'genre': book[3],
            'year': book[4],
            "Quantity": book[5],
            'filename': f'uploads/{book[6]}',
            'id': book[0]
        })
    return render_template("books.html", books=new_result)

@books_bp.route("/loandata")
@login_required
def loandata():
    returndate = request.args.get('return_day')
    user_id = g.user['id']
    book_id = request.args.get('book_id')
    takendateDate = datetime.date.today() 
    #con.cursor().execute(
       # f"INSERT INTO loans ( takendate ,returndate, username,bookid) VALUES (?, ?,?,?)",(returndate,takendateDate),
    return "data accepted"

