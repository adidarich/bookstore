from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html", user=current_user)


@views.route('/books')
def books():
    return render_template("books.html", user=current_user)


@views.route('/add_book')
def add_book():
    return render_template("add_book.html", user=current_user)
