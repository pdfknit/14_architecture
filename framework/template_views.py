# Шаблонный метод
from framework.common import render


class TemplateView:
    template_name = 'base.html'
    page_name = 'Company Name'

    def get_context_data(self):
        context = {}
        class_vars = vars(self.__class__)
        for attr_name, attr_value in class_vars.items():
            if not attr_name.startswith('__') and not callable(attr_value):
                context[attr_name] = attr_value
        print('context -->', context)
        return context
        # return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self):
        # template_name = self.get_template()
        context = self.get_context_data()
        # return '200 OK', render(template_name, **context)
        page = render(**context)
        return '200 OK', [bytes(page, 'UTF-8')]

    def __call__(self, request):
        return self.render_template_with_context()


class ListView(TemplateView):
    queryset = []
    template_name = 'base.html'
    context_object_name = 'objects_list'
    page_name = 'Company Name'

    # def get_queryset(self):
    #     # print(self.queryset)
    #     return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        context = {}
        # queryset = self.get_queryset()
        # context_object_name = self.get_context_object_name()
        # context = {context_object_name: self.queryset, 'page_name': self.page_name}
        class_vars = vars(self.__class__)
        for attr_name, attr_value in class_vars.items():
            if not attr_name.startswith('__') and not callable(attr_value):
                context[attr_name] = attr_value
        print('get_context_data return -->', context)
        return context


class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['post_parameters']  # ['query_parameters']
        # return request['data']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        data = self.get_request_data(request)
        if request['method'] == 'POST':
            # data = self.get_request_data(request)
            self.create_obj(data)
            return self.render_template_with_context()
        else:
            return super().__call__(request)
