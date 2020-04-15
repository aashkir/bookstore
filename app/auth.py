import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # user did a POST, grab the info
        username = request.form['username'] # used to log in (too lazy for password implementation)
        name = request.form['name']
        shipping_info = request.form['shipping_info']
        billing_info = request.form['billing_info']
        db = get_db()
        cursor = db.cursor()
        error = None

        if not username:
            error = 'Username is required.'
        elif not name:
            error = 'name is required.'
        elif not shipping_info:
            error = 'shipping information is required.'
        elif not billing_info:
            error = 'billing information is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            cursor.execute(
                'INSERT INTO user (username, name, shipping_info, billing_info) VALUES (?, ?, ?, ?)',
                (username, name, shipping_info, billing_info)
            )
            id = cursor.lastrowid
            # put the id from the newly created user into customer
            cursor.execute(
                'INSERT INTO customer (id) VALUES (?)', str(id)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        
        if error is None:
            # check if username appears in the owner table, if so, redirect to reports
            session.clear()
            # if the user is also an owner, add it to the session so they can access the reports page
            if db.execute('SELECT id FROM owner WHERE id = ?', (user['id'],)).fetchone() is not None:
                session['is_owner'] = True
            else:
                session['is_owner'] = False
            session['user_id'] = user['id'] # stored in browser cookie, allows access to other parts of website
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    is_owner = session.get('is_owner')

    if user_id is None:
        g.user = None
        g.is_owner = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

        if get_db().execute('SELECT id FROM owner WHERE id = ?', (user_id,)).fetchone() is not None:
            g.is_owner = True

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# use this to force users to login before accessing any page
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
'''
# used for admin access only
def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None and not g.is_owner:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view'''