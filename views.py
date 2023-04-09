from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import AddBook
from app import create_app

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html", user=current_user)


@views.route('/library')
def library():
    return render_template("library.html", user=current_user)


@views.route('/add_book', methods=['GET', 'POST'])
def add_book():
    book = AddBook.query.all()
    return render_template("add_book.html", user=current_user, book=book)
