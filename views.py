from common import render


def index_view(request):
    page_name = 'Company Name'
    text = 'Hi, this is main page of our company'
    abilities = ['Security', '24/7', 'Safety', 'Work for you']
    page = render("templates/index.html", page_name=page_name, text=text, abilities=abilities)
    return '200 OK', [bytes(page, 'UTF-8')]


def contact_view(request):
    contact_info = {'address': 'London, Bakery St. 21'}
    page = render("templates/contacts.html", page_name="Contacts", contact_info=contact_info)
    return '200 OK', [bytes(page, 'UTF-8')]

def not_found_view(request):
    return '404 NOT FOUND', [b'404 NOT FOUND']


if __name__ == '__main__':
    contact_view(request={})
