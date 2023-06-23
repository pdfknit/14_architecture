from wsgiref.simple_server import make_server

from framework.app import Application
from framework.config import DEFAULT_PORT
from urls import routes

application = Application(routes, front_controller={})

with make_server('', DEFAULT_PORT, application) as httpd:
    print(f'Server running on port {DEFAULT_PORT}')
    httpd.serve_forever()
