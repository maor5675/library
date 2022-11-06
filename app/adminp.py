import sqlite3
from flask import Blueprint, render_template, redirect, Flask, request, flash, g


con = sqlite3.connect("books.db", check_same_thread=False)
con.row_factory = sqlite3.Row
cur = con.cursor()
con.commit()

admin_bp = Blueprint('administration', __name__, url_prefix='/administration')

@admin_bp.route("/")
def login():
    return render_template("admin/adminlogin.html")


@admin_bp.route("/logindata", methods=['POST'])
def data():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == "maor" and password == "1234":
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
        return render_template("/admin/admainpage.html",books=new_result)
    else:
        error = 'your username or password its not correct please try again'
        flash(error) 
        return redirect("/auth/login")



