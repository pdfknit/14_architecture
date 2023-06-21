from jinja2 import Template


def create_path(path):
    if len(path) > 1 and path[-1] == '/':
        path = path[:-1]
    return path


def render(template_name, **kwargs):
    with open(template_name, encoding='utf-8') as f:
        template = Template(f.read())
    return template.render(**kwargs)


