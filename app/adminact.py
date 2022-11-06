import os
import sqlite3
from flask import Blueprint, Flask, render_template, request, redirect, session, url_for
from app.books import books
from app.upload import upload_file

con = sqlite3.connect("books.db", check_same_thread=False)
con.row_factory = sqlite3.Row
cur = con.cursor()
con.commit()

# def change_table():
#     cur.execute("ALTER TABLE books ADD filename ")
#     con.commit()
# change_table()

adaction_bp = Blueprint('action', __name__, url_prefix='/administration/action')


@adaction_bp.route("/deletebook")
def deletebook():
    from app.main import app
    id = request.args.get('id')
    cur.execute(f"DELETE FROM books WHERE rowid={id};")
    con.commit()
    return redirect("/administration?message=Book Deleted")

@adaction_bp.route("/addbookindb", methods=['POST'])
def addbook_indb():
    from app.main import app
    title = request.form.get('title')
    author = request.form.get('author')
    genre = request.form.get('genre')
    year = request.form.get('year')
    Quantity = request.form.get('Quantity')
    filename = upload_file(request)
    con.cursor().execute(f"INSERT INTO books (title,author,genre,year,Quantity,filename) VALUES (?, ?, ?, ?, ?, ?)",
    (title,author,genre,year,Quantity,filename))
    con.commit()
    return redirect("/administration?message=Book added")



@adaction_bp.route("/addbook")
def addbook():
    return render_template("/admin/addbook.html")

