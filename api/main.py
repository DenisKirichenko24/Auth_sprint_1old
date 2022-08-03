from core.config import app
from v1.routes import routes
from flask import request



app.register_blueprint(routes)


@app.before_request
def before_request():
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        raise RuntimeError('request id is required')


def main(flask_app):
    flask_app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main(app)
