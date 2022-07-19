from gevent import monkey
from dotenv import load_dotenv

from api.core.config import Config

from gevent.pywsgi import WSGIServer
from api.main import app, main

monkey.patch_all()
load_dotenv()

http_server = WSGIServer(("", Config.FLASK_PORT), main(app))
http_server.serve_forever()
