from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationFrom, TeamSelectionForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from app.tasks import matches, get_match_details

# Renders the home page
@app.route('/')
@app.route('/index')
@login_required # TODO: this maynot be required
def index():
    # Fetch leaderboard from database
    leaderboard = User.query.order_by(User.score.desc()).limit(5)
    # TODO: Live updates to leaderboard
    return render_template('index.html', title='Home', leaderboard = leaderboard)

# Renders the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: # If the user is already logged in
        # TODO: Redirect to where they came from...
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit(): # If the form is being submitted
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # In case of redirects to login
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '': # to prevent redirects to absolute path
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationFrom()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.score = 100
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/myteam', methods=['GET', 'POST'])
def team_selection():
    match_id = int(request.args.get('match_id'))
    match = get_match_details(match_id)

    return render_template('myteam.html', match=match, form=form)