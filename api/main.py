from flask import render_template, request, flash, make_response, jsonify
from flask_admin import Admin

from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from core.config import db, app
from api.models.utils import token_required
from api.models.users import User
import jwt
from datetime import datetime, timedelta


app = app
migrate = Migrate(app, db)
admin = Admin(app)
db = db
db.create_all()


def main(flask_app):
    flask_app.run(debug=True, host='0.0.0.0', port=5001)


# @app.route('/')
# @token_required
# def index():
#     return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    auth = request.form
    print(auth.get('password'))

    if not auth or not auth.get('email') or not auth.get('password'):
        return make_response(
            'Could not login',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )

    user = User.query \
        .filter_by(email=auth.get('email')) \
        .first()

    if not user:
        return make_response(
            'User not found',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )

    if check_password_hash(user.password, auth.get('password')):
        try:
            data = datetime.now() + timedelta(minutes=30)
            token = jwt.encode({
                'id': user.id,
                'exp': data
            }, app.config['SECRET_KEY'])
            return make_response(jsonify({'token': token}), 201)
        except Exception as e:
            print(e)
    return make_response(
        'Could not verify password',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )


@app.route('/signup', methods=['POST'])
def signup():
    data = request.form
    username, email = data.get('username'), data.get('email')
    password = data.get('password')
    user = User.query \
        .filter_by(email=email) \
        .first()
    if not user:

        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        return make_response('Successfully registered.', 201)
    else:
        return make_response('User already exists. Please Log in.', 202)


@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    users = User.query.all()
    output = []
    for user in users:
        output.append({
            'id': user.id,
            'username': user.username,
            'email': user.email
        })

    return jsonify({'users': output})


if __name__ == '__main__':
    main(app)
