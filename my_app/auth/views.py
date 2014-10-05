from flask import request, render_template, flash, redirect, url_for, \
    session, Blueprint, g
from flask.ext.login import current_user, login_user, logout_user, \
    login_required
from my_app import db, login_manager, oid
from my_app.auth.models import User, RegistrationForm, LoginForm, OpenIDForm

auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@auth.before_request
def get_current_user():
    g.user = current_user


@auth.route('/')
@auth.route('/home')
def home():
    return render_template('home.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('username'):
        flash('Your are already logged in.', 'info')
        return redirect(url_for('auth.home'))

    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        password = request.form.get('password')
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
            flash(
                'This username has been already taken. Try another one.',
                'warning'
            )
            return render_template('register.html', form=form)
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered. Please login.', 'success')
        return redirect(url_for('auth.login'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and current_user.is_authenticated():
        flash('You are already logged in.', 'info')
        return redirect(url_for('home'))

    form = LoginForm(request.form)
    openid_form = OpenIDForm(request.form)

    if request.method == 'POST':
        if request.form.has_key('openid'):
            openid_form.validate()
            if openid_form.errors:
                flash(openid_form.errors, 'danger')
                return render_template(
                    'login.html', form=form, openid_form=openid_form
                )
            openid = request.form.get('openid')
            return oid.try_login(openid, ask_for=['email', 'nickname'])
        else:
            form.validate()
            if form.errors:
                flash(form.errors, 'danger')
                return render_template(
                    'login.html', form=form, openid_form=openid_form
                )
            username = request.form.get('username')
            password = request.form.get('password')
            existing_user = User.query.filter_by(username=username).first()

            if not (existing_user and existing_user.check_password(password)):
                flash(
                    'Invalid username or password. Please try again.',
                    'danger'
                )
                return render_template('login.html', form=form)

        login_user(existing_user)
        flash('You have successfully logged in.', 'success')
        return redirect(url_for('auth.home'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('login.html', form=form, openid_form=openid_form)


@oid.after_login
def after_login(resp):
    username = resp.nickname or resp.email
    if not username:
        flash('Invalid login. Please try again.', 'danger')
        return redirect(url_for('auth.login'))
    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username, '')
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for('auth.home'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.home'))
