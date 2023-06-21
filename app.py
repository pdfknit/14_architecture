from common import create_path
from views import not_found_view


class Application:
    def __init__(self, routes, front_controller):
        self.routes = routes
        self.front_controller = front_controller

    def __call__(self, environ, start_response):
        path = create_path(environ['PATH_INFO'])
        if path in self.routes:
            view = self.routes[path]
        else:
            view = not_found_view

        request = {}
        for front_controller in self.front_controller:
            front_controller(request)

        code, body = view(request)
        start_response(code, [('Context-Type', 'text/html')])
        return body
