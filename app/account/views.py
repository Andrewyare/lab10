from flask import  render_template, request, redirect, session, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from .. import  db
from .form import  LoginForm, RegistrationForm
from .models import  User
from . import account_bp

@account_bp.route('/users')
@login_required
def users():
    all_users = User.query.all()
    return render_template('users_data.html', all_users=all_users)

@account_bp.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('account.index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user:
			if user.password == form.password.data:
				login_user(user,remember=form.remember.data)
				flash('You have been logged in!', category='success')
				return redirect(url_for('home.home'))
			else:
				flash('Password is incorrect', category='warning')
				return redirect(url_for('account.login'))
		else:
			flash('Email is incorrect', category='warning') 
	return render_template('login.html', form=form)

@account_bp.route('/user/delete/<id>')
def delete_user_by_id(id):
    data = User.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for("account.users"))

@account_bp.route('/logout')
def logout():
	logout_user()
	flash('You have been logged out')
	return redirect(url_for('home.home'))

@account_bp.route('/account')
def account():
	return render_template('account.html')

@account_bp.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home.home'))
	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		user = User(
			name = form.name.data, 
			email = form.email.data,
			password = form.password.data
			)
		try:
			db.session.add(user)
			db.session.commit()
		except:
			db.session.flush()
			db.session.rollback()
		flash('Thanks for registering')
		return redirect(url_for('home.home'))	
	return render_template('registration.html', form=form)