from flask import render_template, request, flash
from api.core.config import Config
# from flask_auth import models

from flask_migrate import Migrate
from core.config import db, app, manager


app = app
manager = manager
migrate = Migrate(app, db)
db = db
db.create_all()


def main(flask_app):
    flask_app.run(debug=True, host='0.0.0.0', port=5001)


@app.route('/')
def index():
    return render_template('login.html')


# @app.route('/registration', methods=['GET', 'POST'])
# def registration():
#     login = request.form.get('login')
#     password = request.form.get('password')
#     password_confirm = request.form.get('password_confirm')
#     email = request.form.get('email')
#
#     if request.method == 'POST':
#         if not (login or password or password_confirm or email):
#             flash('Please fill all fields')
#
#     if request.method == 'GET':
#         return render_template('registration.html')
#
#
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     login = request.form.get('login')
#     password = request.form.get('password')
#
#     if login and password:
#         user = User.query.filter_by(login=login).first()
#
#         # if check_password_hash(user.password, password):
#         #     login_user(user)
#         #     next = request.args.get('next')
#         #     redirect(next)  # type: ignore
#     else:
#         return render_template('login.html')
#
#
# @app.route('/logout', methods=['GET', 'POST'])
# def logout():
#     pass


if __name__ == '__main__':
    main(app)
