import urllib.parse

from framework.common import render, AppRoute, MapperRegistry
from framework.notifier import EmailNotifier, SmsNotifier
from models import Logger, ObjectCreator
from framework.template_views import ListView, TemplateView
from unit_of_work import UnitOfWork


site = ObjectCreator()
logger = Logger('main')
class_routers = {}
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


@AppRoute(routes=class_routers, url='/')
class IndexView(ListView):
    template_name = 'light/index.html'
    page_name = '!!!Company Name'
    text = 'Hi, this is main page of our company'
    queryset = ['Security', '24/7', 'Safety', 'Work for you']


@AppRoute(routes=class_routers, url='/contacts')
class IndexView(TemplateView):
    template_name = "light/contacts.html"
    contacts_info = {'address': 'London, Bakery St. 22', 'phone': '333-33-33'}
    page_name = "Contacts"


@AppRoute(routes=class_routers, url='/hotels')
def hotels_view(request):
    if request['request_method'] == 'POST':
        post_parameters = request['post_parameters']
        name = post_parameters['name'].replace('+', ' ')
        name = urllib.parse.unquote(name)
        category = None  # пока заглушка на категорию
        new_hotel = site.create_hotel(name, category)
        site.hotels.append(new_hotel)

    page = render("light/hotels.html", hotels=site.hotels)
    return '200 OK', [bytes(page, 'UTF-8')]


@AppRoute(routes=class_routers, url='/hotel_rooms')
def rooms_view(request):
    hotel = site.find_hotel_by_id(int(request['query_parameters']['id']))

    if request['request_method'] == 'POST':
        post_parameters = request['post_parameters']
        name = post_parameters['name'].replace('+', ' ')
        category = 'single'  # пока заглушка на категорию
        room = site.create_room(category, name, hotel)
        room.observers.append(email_notifier)
        room.observers.append(sms_notifier)

        site.rooms.append(room)

    page = render('light/rooms.html',
                  rooms=hotel.rooms,
                  hotel_name=hotel.name, id=hotel.id)

    return '200 OK', [bytes(page, 'UTF-8')]


@AppRoute(routes=class_routers, url='/visitors')
def visitors_view(request):
    if request['request_method'] == 'POST':
        post_parameters = request['post_parameters']
        name = post_parameters['name'].replace('+', ' ')
        name = urllib.parse.unquote(name)
        new_visitor = site.create_user('visitor', name)
        site.visitors.append(new_visitor)
        new_visitor.mark_new()
        UnitOfWork.get_current().commit()

    visitors = MapperRegistry.get_current_mapper('visitors') #достать из базы посетителей
    page = render("light/visitors.html", visitors=visitors.all())

    return '200 OK', [bytes(page, 'UTF-8')]


@AppRoute(routes=class_routers, url='/add_visitor_to_room')
def add_visitors_to_room_view(request):
    if request['request_method'] == 'POST':
        print(request['post_parameters'])
        room = site.find_item_by_id(int(request['post_parameters']['visitor_auto_id']), site.rooms)
        visitor = site.find_item_by_id(int(request['post_parameters']['visitor_auto_id']), site.visitors)
        room.add_visitor(visitor)
    page = render("light/add-visitor-to-room.html", visitors=site.visitors, rooms=site.rooms)
    return '200 OK', [bytes(page, 'UTF-8')]


@AppRoute(routes=class_routers, url='/rooms')
def current_room_view(request):
    print(request)
    room = site.find_item_by_id(int(request['query_parameters']['id']), site.rooms)
    page = render("light/rooms-visitors.html", room=room)
    return '200 OK', [bytes(page, 'UTF-8')]
