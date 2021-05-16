import shutil
import tempfile
from unittest import mock

from django import test
from django.test import override_settings
from model_mommy import mommy

from . import api_test_mixins
from ..models import Image
from ..viewsets import ImageViewSet

# It creates a directory at /tmp/ and set it’s name to the MEDIA_ROOT variable.
MEDIA_ROOT = tempfile.mkdtemp()


class TestList(test.TestCase, api_test_mixins.ListApiTestMixin):
    apiview_class = ImageViewSet

    def test_not_authenticated(self):
        mommy.make('api.Image')
        response = self.make_get_request()
        self.assertEqual(response.status_code, 401)

    def test_ok_user(self):
        requestuser = self.make_user()
        image = mommy.make('api.Image')
        response = self.make_get_request(
            requestuser=requestuser)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0].get('id'), image.id)

    def test_search_image_by_name(self):
        requestuser = self.make_user()
        image = mommy.make('api.Image', name='abra')
        mommy.make('api.Image')
        response = self.make_get_request(
            requestuser=requestuser,
            data={
                'search': 'abr',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(set(self.get_id_list_form_api_response(response)), {image.id})

    def test_search_image_dby_escription(self):
        requestuser = self.make_user()
        image = mommy.make('api.Image', description='cadabra')
        mommy.make('api.Image')
        response = self.make_get_request(
            requestuser=requestuser,
            data={
                'search': 'cad',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(set(self.get_id_list_form_api_response(response)), {image.id})

    def test_search_image_by_portfolio(self):
        requestuser = self.make_user()
        portfolio = mommy.make('api.Portfolio', name='Hotels')
        image = mommy.make('api.Image', portfolio=portfolio)
        mommy.make('api.Image')
        response = self.make_get_request(
            requestuser=requestuser,
            data={
                'search': 'hotels',
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(set(self.get_id_list_form_api_response(response)), {image.id})


class TestRetrieve(test.TestCase, api_test_mixins.RetrieveApiTestMixin):
    apiview_class = ImageViewSet

    def test_get_image_not_authenticated(self):
        image = mommy.make('api.Image')
        response = self.make_get_request(viewkwargs={'pk': image.id})
        self.assertEqual(response.status_code, 401)

    def test_get_image_ok_user(self):
        requestuser = self.make_user()
        image = mommy.make('api.Image')
        response = self.make_get_request(viewkwargs={'pk': image.id}, requestuser=requestuser)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('id'), image.id)

    def test_get_image_ok_response_data(self):
        requestuser = self.make_user()
        portfolio = mommy.make('api.Portfolio', name='Hotels')
        picture = self.generate_image_file('file.png')
        kwargs = {
            'id': 1,
            'name': 'Name',
            'description': 'some description',
            'portfolio': portfolio,
            'upload': picture.name,
            'created_by': requestuser,
        }

        image = mommy.make('api.Image', **kwargs)
        comments = mommy.make('api.Comment', image=image, comment='some comment')

        response = self.make_get_request(viewkwargs={'pk': image.id}, requestuser=requestuser)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.data.keys()), {
            'created_datetime',
            'created_by',
            'name',
            'description',
            'portfolio',
            'upload',
            'id',
            'comments',
        })
        self.assertEqual(response.data.get('id'), image.id)
        self.assertEqual(response.data.get('name'), 'Name')
        self.assertEqual(response.data.get('description'), 'some description')
        self.assertEqual(response.data.get('portfolio'), portfolio.id)
        self.assertEqual(response.data.get('comments'), [comments.id])
        self.assertEqual(response.data.get('upload'), f'http://testserver/media/{picture.name}')


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TestPatch(test.TestCase, api_test_mixins.PatchApiTestMixin):
    apiview_class = ImageViewSet

    # to delete the temporery directory at MADIA_ROOT
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_image_update_not_authenticated(self):
        image = mommy.make('api.Image')
        response = self.make_patch_request(viewkwargs={'pk': image.id})
        self.assertEqual(response.status_code, 401)

    def test_image_update_nok_user(self):
        requestuser = self.make_user()
        image = mommy.make('api.Image')
        response = self.make_patch_request(viewkwargs={'pk': image.id}, requestuser=requestuser)
        self.assertEqual(response.status_code, 403)

    def test_image_update_ok_user(self):
        requestuser = self.make_user()
        image = mommy.make('api.Image', created_by=requestuser)
        response = self.make_patch_request(viewkwargs={'pk': image.id}, requestuser=requestuser)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('id'), image.id)

    def test_image_update_ok_response_data(self):
        requestuser = self.make_user()
        portfolio = mommy.make('api.Portfolio', name='Hotels')
        picture = self.generate_image_file('hotel_1.jpg')
        kwargs = {
            'id': 1,
            'name': 'Name',
            'description': 'some description',
            'portfolio': portfolio,
            'upload': picture.name,
            'created_by': requestuser,
        }

        image = mommy.make('api.Image', **kwargs)
        picture_2 = self.generate_image_file('hotel_2.jpg')

        portfolio_2 = mommy.make('api.Portfolio', name='Films', created_by=requestuser)
        request_data = {
            'name': 'Other_Name',
            'description': 'other_description',
            'upload': picture_2,
            'portfolio': portfolio_2.id,
        }

        response = self.make_patch_request(viewkwargs={'pk': image.id}, requestuser=requestuser, data=request_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('id'), image.id)
        self.assertEqual(response.data.get('name'), 'Other_Name')
        self.assertEqual(response.data.get('description'), 'other_description')
        self.assertEqual(response.data.get('portfolio'), portfolio_2.id)
        self.assertEqual(response.data.get('upload'), f'http://testserver/media/user_{requestuser.id}/Films/{picture_2.name}')


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class TesCreate(test.TestCase, api_test_mixins.CreateApiTestMixin):
    apiview_class = ImageViewSet

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_image_create_not_authenticated(self):
        response = self.make_post_request(data={})
        self.assertEqual(response.status_code, 401)

    def test_image_create_ok(self):
        requestuser = self.make_user()
        portfolio = mommy.make('api.Portfolio', name='Hotels')
        picture = self.generate_image_file('hotel_1.jpg')
        data = {
            'name': 'Name',
            'description': 'some_description',
            'portfolio': portfolio.id,
            'upload': picture,
        }
        self.assertEqual(Image.objects.count(), 0)
        response = self.make_post_request(data=data, requestuser=requestuser)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Image.objects.count(), 1)
        image = Image.objects.first()
        self.assertEqual(image.name, 'Name')
        self.assertEqual(image.description, 'some_description')
        self.assertEqual(image.portfolio.name, 'Hotels')
        self.assertEqual(response.data.get('upload'), f'http://testserver/media/user_{requestuser.id}/Hotels/{picture.name}')


    def test_image_create_without_name(self):
        requestuser = self.make_user()
        portfolio = mommy.make('api.Portfolio', name='Hotels')
        picture = self.generate_image_file('hotel_1.jpg')
        data = {
            'description': 'some_description',
            'portfolio': portfolio.id,
            'upload': picture,
        }
        response = self.make_post_request(data=data, requestuser=requestuser)
        self.assertEqual(response.status_code, 400)

    def test_image_create_without_portfolio(self):
        requestuser = self.make_user()
        # portfolio = mommy.make('api.Portfolio', name='Hotels')
        picture = self.generate_image_file('hotel_1.jpg')
        data = {
            'name': 'Name',
            'description': 'some_description',
            # 'portfolio': portfolio.id,
            'upload': picture,
        }
        response = self.make_post_request(data=data, requestuser=requestuser)
        self.assertEqual(response.status_code, 400)

    def test_image_create_without_description(self):
        requestuser = self.make_user()
        portfolio = mommy.make('api.Portfolio', name='Hotels')
        picture = self.generate_image_file('hotel_1.jpg')
        data = {
            'name': 'Name',
            # 'description': 'some_description',
            'portfolio': portfolio.id,
            'upload': picture,
        }
        response = self.make_post_request(data=data, requestuser=requestuser)
        self.assertEqual(response.status_code, 400)

    def test_image_create_without_upload(self):
        requestuser = self.make_user()
        portfolio = mommy.make('api.Portfolio', name='Hotels')
        picture = self.generate_image_file('hotel_1.jpg')
        data = {
            'name': 'Name',
            'description': 'some_description',
            'portfolio': portfolio.id,
            # 'upload': picture,
        }
        response = self.make_post_request(data=data, requestuser=requestuser)
        self.assertEqual(response.status_code, 400)

    def test_image_create_with_too_big_upload_file(self):
        requestuser = self.make_user()
        portfolio = mommy.make('api.Portfolio', name='Hotels')
        picture = self.generate_image_file('hotel_1.jpg')
        data = {
            'name': 'Name',
            'description': 'some_description',
            'portfolio': portfolio.id,
            'upload': picture,
        }
        with mock.patch('api.serializers.image.MAX_FILE_SIZE', 100):
            response = self.make_post_request(data=data, requestuser=requestuser)
        self.assertEqual(response.status_code, 400)



class TesDelete(test.TestCase, api_test_mixins.DeleteApiTestMixin):
    apiview_class = ImageViewSet

    def test_image_delete_not_authenticated(self):
        image = mommy.make('api.Image')
        response = self.make_delete_request(viewkwargs={'pk': image.id})
        self.assertEqual(response.status_code, 401)

    def test_image_delete_nok_user(self):
        requestuser = self.make_user()
        image = mommy.make('api.Image')
        response = self.make_delete_request(viewkwargs={'pk': image.id}, requestuser=requestuser)
        self.assertEqual(response.status_code, 403)

    def test_image_delete_no_image(self):
        requestuser = self.make_user()
        response = self.make_delete_request(viewkwargs={'pk': 1},
                                            requestuser=requestuser)
        self.assertEqual(response.status_code, 404)

    def test_image_delete_ok_destroy(self):
        requestuser = self.make_user()
        image = mommy.make('api.Image', created_by=requestuser)
        response = self.make_delete_request(viewkwargs={'pk': image.id},
                                            requestuser=requestuser)
        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Image.DoesNotExist):
            image.refresh_from_db()
