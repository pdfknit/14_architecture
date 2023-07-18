# Буду делать сеть отелей. Продумать структуру
# Пользователи - посетитель отеля, администратор отеля
# ЮзерФабрика: создание пользователя или бронирующего номера или управляющего бронированием
# Отели разного типа
# Комнаты внутри отеля разного типа


from copy import deepcopy

# Пользователи - посетитель отеля, администратор отеля
# from framework.common import Subject
from framework.notifier import Subject
from unit_of_work import DomainObject


class User:
    auto_id = 1

    def __init__(self, name):
        self.name = name
        self.auto_id = User.auto_id
        User.auto_id += 1
        # super().__init__()


class Visitor(User, DomainObject):
    # pass
    def __init__(self, name):
        self.rooms = []
        super().__init__(name)


class HotelAdministrator(User):
    pass


# ЮзерФабрика: создание пользователя или бронирующего номера или управляющего бронированием
class UserFactory:
    types = {
        'visitor': Visitor,
        'hotel_administator': HotelAdministrator,
    }

    @classmethod
    def create_user(cls, users_type, name):
        return cls.types[users_type](name)


class RoomPrototype:
    def clone(self):
        return deepcopy(self)


# Комнаты разного типа в отеле
class Room(RoomPrototype, Subject):
    auto_id = 1

    def __init__(self, name, hotel):
        self.auto_id = Room.auto_id
        Room.auto_id += 1
        self.name = name
        self.hotel = hotel
        self.hotel.rooms.append(self)
        self.visitors = []
        super().__init__()

    def __getitem__(self, item):
        return self.visitors[item]

    def add_visitor(self, visitor: Visitor):
        self.visitors.append(visitor)
        visitor.rooms.append(self)
        self.notify()


class SingleRoom(Room):
    pass


class DoubleRoom(Room):
    pass


class TripleRoom(Room):
    pass


class BedInRoom(Room):
    pass


class RoomFactory:
    types = {
        'single': SingleRoom,
        'double': DoubleRoom,
        'triple': TripleRoom,
        'bed': BedInRoom,
    }

    @classmethod
    def create(cls, rooms_type, name, hotel):
        return cls.types[rooms_type](name, hotel)


# Отели разного типа, в которых будут комнаты
class Hotel:
    auto_id = 1

    def __init__(self, name, hotel_type='hotel'):
        self.id = Hotel.auto_id
        Hotel.auto_id += 1
        self.name = name
        self.hotel_type = hotel_type
        self.rooms = []

    def count_rooms(self):
        rooms = len(self.rooms)
        return rooms

    def __str__(self):
        return self.name


class ApartHotel(Hotel):
    pass


class Hostel(Hotel):
    pass


class ClassicHotel(Hotel):
    pass


# Фабрика отелей для содания отелей разного типа
class HotelFactory:
    types = {
        'apart': ApartHotel,
        'hostel': Hostel,
        'hotel': ClassicHotel,
    }

    @classmethod
    def create_hotel(cls, hotels_type):
        return cls.types[hotels_type]()


# Класс-создатель
class ObjectCreator:
    def __init__(self):
        self.visitors = []
        self.admins = []
        self.hotels = []
        self.rooms = []

    @staticmethod
    def create_user(users_type, name):
        return UserFactory.create_user(users_type, name)

    @staticmethod
    def create_hotel(name, hotel_type):
        return Hotel(name, hotel_type)

    def find_item_by_id(self, id, items):
        for item in items:
            if item.auto_id == id:
                return item
        raise Exception(f'Нет элемента с id = {id}')

    def find_hotel_by_id(self, id):
        for hotel in self.hotels:
            print('hotel', hotel.id)
            if hotel.id == id:
                return hotel
        raise Exception(f'Нет отеля с id = {id}')

    def find_room_by_id(self, id):
        for item in self.rooms:
            if item.auto_id == id:
                return item

    def find_visitor_by_id(self, id):
        for item in self.visitors:
            if item.auto_id == id:
                return item

    @staticmethod
    def create_room(rooms_type, name, hotel):
        return RoomFactory.create(rooms_type, name, hotel)

    def get_room(self, name):
        for room in self.rooms:
            if room.name == name:
                return room
        return None


# Синглтон
class Singletons(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=Singletons):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('----->', text)
