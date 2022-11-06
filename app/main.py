from flask import Flask, redirect, url_for
from app.upload import upload_bp
from app.books import books_bp
from app.login import auth_bp
from app.adminp import admin_bp
from app.adminact import adaction_bp



UPLOAD_FOLDER = './app/static/uploads'
DOWLOAD_FOLDER = './static/uploads'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWLOAD_FOLDER'] = DOWLOAD_FOLDER
app.register_blueprint(upload_bp)
app.register_blueprint(books_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(adaction_bp)
app.secret_key = 'asfajkbasdpgou0-31r98t6dshvl'
@app.route("/")
def main():
    return redirect(url_for('books.books'))

if __name__ == "__main__":
  app.run(debug=True)