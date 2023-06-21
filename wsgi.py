def application(environ, start_response):
    start_response('200 OK', [('Context-Type', 'text/html')])
    return [b'Hello, world!']