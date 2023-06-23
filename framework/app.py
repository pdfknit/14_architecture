from framework.common import create_path, parse_input_data, bytes_to_dict, get_post_data, decode_value


class PageNotFound404:
    def __call__(self, request):
        return '404 NOT FOUND', [b'404 NOT FOUND']


class Application:
    def __init__(self, routes, front_controller):
        self.routes = routes
        self.front_controller = front_controller

    def __call__(self, environ, start_response):

        path_info = create_path(environ['PATH_INFO'])
        if path_info in self.routes:
            view = self.routes[path_info]
        else:
            view = PageNotFound404()

        request = {
            'request_method': environ['REQUEST_METHOD']
        }

        if request['request_method'] == 'GET':
            query_dict = parse_input_data(environ['QUERY_STRING'])
            print('GET запрос с параметрами:', query_dict)

        if request['request_method'] == 'POST':
            post_data = get_post_data(environ)
            query_dict = decode_value(bytes_to_dict(post_data))
            # query_dict = bytes_to_dict(post_data)
            print('POST запрос с параметрами:', query_dict)

        for front_controller in self.front_controller:
            front_controller(request)

        code, body = view(request)
        start_response(code, [('Context-Type', 'text/html')])
        return body
