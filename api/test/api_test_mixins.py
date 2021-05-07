import io

from django.conf import settings
from model_mommy import mommy
from rest_framework.test import APIRequestFactory, force_authenticate
from PIL import Image


class ApiTestMixin:
    """
    Mixin class for API tests.
    Can be used for ViewSets too. Just override :meth:`.get_as_view_kwargs` - see example in the docs
    for that method.
    """
    apiview_class = None

    def get_default_requestuser(self):
        return None

    def make_user(self, email='user@example.com', **kwargs):
        return mommy.make(settings.AUTH_USER_MODEL, email=email, **kwargs)

    def get_as_view_kwargs(self):
        """
        The kwargs for the ``as_view()``-method of the API view class.

        If you are writing tests for a ViewSet, you have to override this
        to define what action you are testing (list, retrieve, update, ...), like this::

            def get_as_view_kwargs(self):
                return {
                    'actions: {
                        'get': 'list'
                    }
                }
        """
        return {}

    def add_authenticated_user_to_request(self, request, requestuser):
        if requestuser:
            force_authenticate(request, requestuser)

    def make_request(self, method, viewkwargs=None, api_url='/test/', data=None, requestuser=None):
        factory = APIRequestFactory()
        request = getattr(factory, method)(api_url, format='json', data=data)
        viewkwargs = viewkwargs or {}
        if requestuser:
            # request.user = requestuser or self.get_default_requestuser()
            self.add_authenticated_user_to_request(request, requestuser)
        response = self.apiview_class.as_view(**self.get_as_view_kwargs())(request, **viewkwargs)
        response.render()
        return response

    def make_get_request(self, viewkwargs=None, api_url='/test/', data=None, requestuser=None):
        return self.make_request(method='get', viewkwargs=viewkwargs,
                                 api_url=api_url, data=data,
                                 requestuser=requestuser)

    def make_post_request(self, viewkwargs=None, api_url='/test/', data=None, requestuser=None):
        return self.make_request(method='post', viewkwargs=viewkwargs,
                                 api_url=api_url, data=data,
                                 requestuser=requestuser)

    def make_put_request(self, viewkwargs=None, api_url='/test/', data=None, requestuser=None):
        return self.make_request(method='put', viewkwargs=viewkwargs,
                                 api_url=api_url, data=data,
                                 requestuser=requestuser)

    def make_delete_request(self, viewkwargs=None, api_url='/test/', data=None, requestuser=None):
        return self.make_request(method='delete', viewkwargs=viewkwargs,
                                 api_url=api_url, data=data,
                                 requestuser=requestuser)

    def get_id_list_form_api_response(self, response):
        return [obj.get('id') for obj in response.data['results']]

    def generate_image_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file


class CreateApiTestMixin(ApiTestMixin):
    def get_as_view_kwargs(self):
        return {
            'actions': {
                'post': 'create'
            }
        }


class ListApiTestMixin(ApiTestMixin):
    def get_as_view_kwargs(self):
        return {
            'actions': {
                'get': 'list'
            }
        }


class RetrieveApiTestMixin(ApiTestMixin):
    def get_as_view_kwargs(self):
        return {
            'actions': {
                'get': 'retrieve'
            }
        }


class PatchApiTestMixin(ApiTestMixin):
    def get_as_view_kwargs(self):
        return {
            'actions': {
                'patch': 'partial_update'
            }
        }

    def make_patch_request(self, viewkwargs=None, api_url='/test/', data=None, requestuser=None):
        return self.make_request(method='patch', viewkwargs=viewkwargs,
                                 api_url=api_url, data=data,
                                 requestuser=requestuser)


class DeleteApiTestMixin(ApiTestMixin):
    def get_as_view_kwargs(self):
        return {
            'actions': {
                'delete': 'destroy'
            }
        }
