from functools import wraps
import time
import jwt

from redis import Redis

from api.core.config import app, Config, api
from flask import request, jsonify

from .users import User

REQUEST_LIMIT_PER_MINUTE = 5
config = Config()
r = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'access_token' in request.headers:
            token = request.headers['access_token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(
                token, app.config['SECRET_KEY'],
                algorithms=["HS256"],
                verify_exp=True
            )
            current_user = User.query \
                .filter_by(id=data['id']) \
                .first()
        except jwt.ExpiredSignatureError:
            return jsonify({  # redirect to refresh
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users context to the routes
        return f(current_user, *args, **kwargs)

    return decorated


def refresh_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'refresh_token' in request.headers:
            token = request.headers['refresh_token']
            return f(token, *args, **kwargs)
        return jsonify({
            'message': 'Refresh token is invalid !!'
        }), 401

    return decorated


def rate_limit(limit=10, interval=60, shared_limit=True, key_prefix="rl"):
    def rate_limit_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            t = int(time.time())
            closest_minute = t - (t % interval)
            if shared_limit:
                key = "%s:%s:%s" % (key_prefix, request.remote_addr, closest_minute)
            else:
                key = "%s:%s:%s.%s:%s" % (key_prefix, request.remote_addr,
                                          f.__module__, f.__name__, closest_minute)
            current = r.get(key)

            if current and int(current) > limit:
                retry_after = interval - (t - closest_minute)
                resp = jsonify({
                    'code': 429,
                    "message": "Too many requests. Limit %s in %s seconds" % (limit, interval)
                })
                resp.status_code = 429
                resp.headers['Retry-After'] = retry_after
                return resp
            else:
                pipe = r.pipeline()
                pipe.incr(key, 1)
                pipe.expire(key, interval + 1)
                pipe.execute()

                return f(*args, **kwargs)

        return wrapper

    return rate_limit_decorator
