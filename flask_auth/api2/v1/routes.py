from flask import flash, render_template, request

from api.main import app
from api.models import User


@app.route('/')
def index():
    return render_template('login.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    login = request.form.get('login')
    password = request.form.get('password')
    password_confirm = request.form.get('password_confirm')
    email = request.form.get('email')

    if request.method == 'POST':
        if not (login or password or password_confirm or email):
            flash('Please fill all fields')

    if request.method == 'GET':
        return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()

        # if check_password_hash(user.password, password):
        #     login_user(user)
        #     next = request.args.get('next')
        #     redirect(next)  # type: ignore
    else:
        return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    pass
