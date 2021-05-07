from django import test
from model_mommy import mommy

from . import api_test_mixins
from ..viewsets import ImageViewSet


class TestList(test.TestCase, api_test_mixins.ListApiTestMixin):
    apiview_class = ImageViewSet

    def test_not_authenticated(self):
        mommy.make('api.Image')
        response = self.make_get_request()
        self.assertEqual(response.status_code, 403)

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
        print('=====', response.data)
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

    def test_not_authenticated(self):
        image = mommy.make('api.Image')
        response = self.make_get_request(viewkwargs={'pk': image.id})
        self.assertEqual(response.status_code, 403)

    def test_ok_user(self):
        requestuser = self.make_user()
        image = mommy.make('api.Image')
        response = self.make_get_request(viewkwargs={'pk': image.id}, requestuser=requestuser)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('id'), image.id)

    def test_ok_response_data(self):
        requestuser = self.make_user()
        portfolio = mommy.make('api.Portfolio', name='Hotels')
        picture = self.generate_photo_file()
        kwargs = {
            'id': 1,
            'name': 'Name',
            'description': 'some description',
            'portfolio': portfolio,
            'upload': picture.name
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
        print(dir(picture))
        self.assertEqual(response.data.get('id'), image.id)
        self.assertEqual(response.data.get('name'), 'Name')
        self.assertEqual(response.data.get('description'), 'some description')
        self.assertEqual(response.data.get('portfolio'), portfolio.id)
        self.assertEqual(response.data.get('comments'), [comments.id])
        self.assertEqual(response.data.get('upload'), f'http://testserver/media/{picture.name}')


# class TestPatch(test.TestCase, api_test_mixins.PatchApiTestMixin):
#     apiview_class = CustomerViewSet
#
#     def test_not_authenticated(self):
#         customer = mommy.make('buyclip_core.Customer')
#         response = self.make_patch_request(viewkwargs={'pk': customer.id},
#                                            data={'name': 'New name'})
#         self.assertEqual(response.status_code, 403)
#
#     def test_no_customer(self):
#         requestuser = self.make_superuser()
#         response = self.make_patch_request(viewkwargs={'pk': 1}, requestuser=requestuser,
#                                            data={'name': 'New name'})
#         self.assertEqual(response.status_code, 404)
#
#     def test_ok_superuser(self):
#         requestuser = self.make_superuser()
#         customer = mommy.make('buyclip_core.Customer')
#         response = self.make_patch_request(viewkwargs={'pk': customer.id}, requestuser=requestuser,
#                                            data={'comment': 'comment'})
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data.get('id'), customer.id)
#
#     def test_ok_user(self):
#         requestuser = self.make_user()
#         customer = mommy.make('buyclip_core.Customer')
#         response = self.make_patch_request(viewkwargs={'pk': customer.id}, requestuser=requestuser,
#                                            data={'comment': 'comment'})
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.data.get('id'), customer.id)
#
#     def test_ok_response_data(self):
#         requestuser = self.make_user()
#         kwargs = {
#             'id': 1,
#             'name': 'Name',
#             'email': 'abra@cadabra.com',
#             'extra_data': {'some': 'data'},
#             'phone_number': '1234',
#             'address': 'some_address'
#         }
#
#         customer = mommy.make('buyclip_core.Customer', **kwargs)
#         request_data = {
#             'name': 'new_Name',
#             'email': 'new@new.com',
#             'extra_data': {'some': 'other'},
#             'phone_number': '5678',
#             'address': 'other_address'
#         }
#
#         response = self.make_patch_request(viewkwargs={'pk': customer.id}, requestuser=requestuser,
#                                            data=request_data)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(set(response.data.keys()), {
#             'last_updated_datetime',
#             'created_datetime',
#             'last_updated_by',
#             'created_by',
#             'extra_data',
#             'name',
#             'email',
#             'phone_number',
#             'address',
#             'id',
#         })
#         self.assertEqual(response.data.get('id'), customer.id)
#         self.assertEqual(response.data.get('name'), 'new_Name')
#         self.assertEqual(response.data.get('email'), 'new@new.com')
#         self.assertEqual(response.data.get('extra_data'), {'some': 'other'})
#         self.assertEqual(response.data.get('phone_number'), '5678')
#         self.assertEqual(response.data.get('address'), 'other_address')
#
#
# class TesCreate(test.TestCase, api_test_mixins.CreateApiTestMixin):
#     apiview_class = CustomerViewSet
#
#     def test_not_authenticated(self):
#         response = self.make_post_request(data={})
#         self.assertEqual(response.status_code, 403)
#
#     def test_ok(self):
#         requestuser = self.make_user()
#         data = {
#             'name': 'Name',
#             'email': 'abra@cadabra.com',
#             'extra_data': {'some': 'data'},
#             'phone_number': '1234',
#             'address': 'some_address'
#         }
#         self.assertEqual(Customer.objects.count(), 0)
#         response = self.make_post_request(data=data, requestuser=requestuser)
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(Customer.objects.count(), 1)
#         customer = Customer.objects.first()
#         self.assertEqual(customer.name, 'Name')
#         self.assertEqual(customer.email, 'abra@cadabra.com')
#         self.assertEqual(customer.extra_data, {'some': 'data'})
#         self.assertEqual(customer.phone_number, '1234')
#         self.assertEqual(customer.address, 'some_address')
#
#
# class TesDelete(test.TestCase, api_test_mixins.DeleteApiTestMixin):
#     apiview_class = CustomerViewSet
#
#     def test_not_authenticated(self):
#         customer = mommy.make('buyclip_core.Customer')
#         response = self.make_delete_request(viewkwargs={'pk': customer.id})
#         self.assertEqual(response.status_code, 403)
#
#     def test_no_customer(self):
#         requestuser = self.make_superuser()
#         response = self.make_delete_request(viewkwargs={'pk': 1},
#                                             requestuser=requestuser)
#         self.assertEqual(response.status_code, 404)
#
#     def test_ok_destroy(self):
#         requestuser = self.make_user()
#         customer = mommy.make('buyclip_core.Customer')
#         response = self.make_delete_request(viewkwargs={'pk': customer.id},
#                                             requestuser=requestuser)
#         self.assertEqual(response.status_code, 204)
#         with self.assertRaises(Customer.DoesNotExist):
#             customer.refresh_from_db()
