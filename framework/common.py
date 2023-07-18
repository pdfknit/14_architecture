import urllib.parse
from sqlite3 import connect

from jinja2 import Environment, FileSystemLoader
from framework.config import DEFAULT_TEMPLATES_FOLDER, DATABASE_NAME
from models import Visitor


def create_path(path: str) -> str:
    if len(path) > 1 and path[-1] == '/':
        path = path[:-1]
    return path


def render(template_name, folder=DEFAULT_TEMPLATES_FOLDER, **kwargs):
    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
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
        urllib_decode_str = urllib.parse.unquote(v)
        new_data[k] = urllib_decode_str
    return new_data


# Декоратор
class AppRoute:
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        # так как у меня микс из классов и функций для вьюшек, то проверяю функция ли это и, если нет, то добавляю ее вызываемой
        if isinstance(cls, type):
            self.routes[self.url] = cls()
        else:
            self.routes[self.url] = cls

#
# # Наблюдатель
# class Observer:
#
#     def update(self, subject):
#         pass


# class Subject:
#
#     def __init__(self):
#         self.observers = []
#
#     def notify(self):
#         for item in self.observers:
#             item.update(self)
#
#
# class SmsNotifier(Observer):
#
#     def update(self, subject):
#         print('SMS->', 'к нам присоединился', subject.visitors[-1].name)
#
#
# class EmailNotifier(Observer):
#
#     def update(self, subject):
#         print(('EMAIL->', 'к нам присоединился', subject.visitors[-1].name))



class VisitorMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'visitors'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            visitor = Visitor(name)
            visitor.auto_id = id
            result.append(visitor)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, name FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Visitor(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (name) VALUES (?)"
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET name=? WHERE id=?"

        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


connection = connect(DATABASE_NAME)


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {
        'visitors': VisitorMapper,
        #'category': CategoryMapper
    }

    @staticmethod
    def get_mapper(obj):

        if isinstance(obj, Visitor):

            return VisitorMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')




