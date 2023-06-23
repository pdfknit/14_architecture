from framework.app import PageNotFound404
from views import index_view, contact_view

routes = {
    '/': index_view,
    '/contacts': contact_view,
    '/404': PageNotFound404(),
    '/index': index_view,
}
