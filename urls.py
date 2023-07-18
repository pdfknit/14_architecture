from framework.app import PageNotFound404
from views import class_routers, IndexView

routes = {
    '/404': PageNotFound404(),
    # '/index2': IndexView()
}
# print('class_routers', class_routers)
routes.update(class_routers)
# print('routes', routes)