from flask import request, make_response, jsonify
from redis import Redis

from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_jwt_extended import create_refresh_token, JWTManager
from core.config import db, app, Config
from api.models.utils import token_required, refresh_token_required
from api.models.users import User
import jwt
from datetime import datetime, timedelta, timezone
from core.redis import RedisStorage

app = app
migrate = Migrate(app, db)
db = db
db.create_all()
app.config['JWT_SECRET_KEY'] = 'secret_jwt_key'
ref = JWTManager(app)
config = Config()
redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)
token_storage = RedisStorage(redis)
token_expire = 43200  # время действия токена(месяц)


def main(flask_app):
    flask_app.run(debug=True, host='0.0.0.0', port=5001)


# @app.route('/')
# @token_required
# def index():
#     return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    auth = request.form

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
            time_data = datetime.now(tz=timezone.utc) + timedelta(seconds=1)
            token = jwt.encode({
                'id': user.id,
                'exp': time_data
            }, app.config['SECRET_KEY'])
            refresh_token = create_refresh_token(identity=user.password)
            token_storage.set(refresh_token, user.id, token_expire)
            return make_response(jsonify({'access_token': token}, {'refresh_token': refresh_token}), 201)
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


@app.route('/refresh', methods=['POST'])
@refresh_token_required
def refresh_token(refresh_token):
    user_id = token_storage.get(refresh_token)
    token_storage.remove(refresh_token)
    time_data = datetime.now() + timedelta(minutes=30)
    token = jwt.encode({
        'id': user_id,
        'exp': time_data
    }, app.config['SECRET_KEY'])
    refresh_token = create_refresh_token(identity=user_id)
    token_storage.set(refresh_token, user_id, token_expire)
    print(token)
    print(refresh_token)
    return make_response(jsonify({'new_access_token': token}, {'new_refresh_token': refresh_token}), 201)


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
