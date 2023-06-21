from views import index_view, contact_view, not_found_view

routes = {
    '/': index_view,
    '/contacts': contact_view,
    '/404': not_found_view,
}
