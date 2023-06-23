import requests
import urllib.parse

from jinja2 import Template
from quopri import decodestring


def create_path(path: str) -> str:
    if len(path) > 1 and path[-1] == '/':
        path = path[:-1]

    # sample from lesson
    # if not path.endswith('/'):
    #     path = f'{path}/'
    return path


def render(template_name, **kwargs):
    with open(template_name, encoding='utf-8') as f:
        template = Template(f.read())
    return template.render(**kwargs)


def parse_input_data(data) -> dict:
    parameters = {}
    if data:
        items = data.split('&')
        for item in items:
            key, value = item.split('=')
            value = urllib.parse.unquote(value)
            parameters[key] = value
    return parameters


def get_post_data(environ) -> bytes:
    if environ.get('CONTENT_LENGTH'):
        content_length = int(environ.get('CONTENT_LENGTH'))
        post_data = environ['wsgi.input'].read(content_length)
    else:
        post_data = b''
    return post_data


def bytes_to_dict(data: bytes) -> dict:
    result = {}

    if data:
        string_data = data.decode('utf-8')
        result = parse_input_data(string_data)
    return result


def decode_value(data: dict) -> dict:
    new_data = {}
    for k, v in data.items():
        # val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
        # val_decode_str = decodestring(val).decode('UTF-8')
        urllib_decode_str = urllib.parse.unquote(v)
        new_data[k] = urllib_decode_str
    return new_data
