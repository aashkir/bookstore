from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db

bp = Blueprint('bookstore', __name__)
@bp.route('/')
@login_required
def index():
    db = get_db()
    # grab books fom db
    books = db.execute(
        'SELECT ISBN, title, num_pages, price'
        ' FROM book'
    ).fetchall()
    print(books)
    return render_template('bookstore/index.html', books=books)