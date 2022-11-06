import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint('auth', __name__, url_prefix='/auth')

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def get_db():
    from app.books import con
    return con

@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        address = request.form['address']
        email = request.form['email']
        phonenumber = request.form['phonenumber']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if not email:
            error = 'email is required.'
        elif not address:
            error = 'address is required.'

        if not phonenumber:
            error = 'phone number is required.'     
        
        if error is None:
            try:
                db.cursor().execute(
                    "INSERT INTO user (username, password, email, address, phonenumber) VALUES (?, ?, ?, ?,?)",
                    (username, generate_password_hash(password),email,address,phonenumber),
                )
                db.commit()
            except Exception as ex:
                error = f"ex"
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.cursor().execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            global use_user
            use_user = user['id']
            session['user_id'] = user['id']
            return redirect(url_for('books.books'))

        flash(error)

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('books.books'))

def name():
    return use_user