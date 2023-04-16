from flask import Blueprint, flash, render_template, request, redirect, url_for, send_from_directory
from flask_login import login_required, current_user
from models import User, AddBook
from app import db, create_app

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template("home.html", user=current_user)


@views.route('/user/<first_name>')
@login_required
def user(first_name):
    user = User.query.filter_by(first_name=first_name).first()
    if user == None:
        flash('User' + first_name + ' not found.')
        return redirect(url_for('home'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #1'},
    ]
    return render_template('account.html', user=user, posts=posts)


@views.route('/library')
def library():
    books = AddBook.query.all()
    return render_template("library.html", books=books, user=current_user)


@views.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(create_app().config['UPLOAD_FOLDER'], filename)


@views.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        pl = request.form['pl']
        cover = request.form['cover']
        description = request.form['description']

        if len(title) < 1:
            flash('Don`t must be empty', category='error')
        else:
            addbook = AddBook(title=title,
                              author=author,
                              pl=pl,
                              cover=cover,
                              description=description,
                              user_id=current_user.id)
            db.session.add(addbook)
            db.session.commit()
            flash('the book was added successfully', category='success')
    #         return redirect(url_for('library'))

    return render_template("add_book.html", user=current_user)
