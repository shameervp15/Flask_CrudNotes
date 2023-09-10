from flask import request, render_template, redirect, url_for, flash
from website.models import User
from website import db, bcrypt
from flask_login import login_required, current_user, logout_user, login_user
from website.user.forms import RegistrationForm, LoginForm, UpdateUserForm, RequestResetForm, ResetPasswordForm
from website.user.utils import send_reset_mail, save_picture

from flask import Blueprint

user = Blueprint('user', __name__)


@user.route('/sign-up', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.first_name.data}!', category='success')
        return redirect(url_for('user.login'))
    return render_template('signup.html', user=current_user, form=form)
            
@user.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            nextpage = request.args.get('next')
            flash('Logged in!', category='success')
            return redirect(nextpage) if nextpage else redirect(url_for('notes.home'))
        else:
            flash('Username and Password Does not Match!', category='error')
            print(form.email.data)
    return render_template('login.html', user=current_user, form=form)

   
@user.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user.login'))


@user.route('/reset-password', methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        redirect(url_for('user.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_mail(user)
        flash('The verification email has been sent to the mail.', category="success")
    return render_template('reset_request.html', form=form, user=current_user)

@user.route('/reset-password/<token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        redirect(url_for('user.home'))
    user = User.verify_token(token)
    if user is None:
        flash('The token has been expired or invalid!', category='warning')
        return redirect(url_for('user.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pwd
        db.session.commit()
        flash('Password successfully changed!')
        return redirect(url_for('user.login'))
    return render_template('reset_token.html', form=form)

@user.route('/account', methods=['POST','GET'])
@login_required
def account():
    imgfile = url_for('static', filename='/profilepics/' + current_user.imgfile)
    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.imgfile = picture_file
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        db.session.commit()
        flash('Account updates successfully!', category='success')
        return redirect(url_for('user.account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
    return render_template('account.html', user=current_user, form=form, img=imgfile)