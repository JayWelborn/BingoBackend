from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.test import APITestCase, APIRequestFactory

from api.viewsets import UserViewset

import pdb


class UserViewsetTests(APITestCase):
    """Tests for User View Set.

    Methods:
        setUp: Create test users
        tearDown: Empty test database
        test_user_list_on_get: `GET` requests with no `pk` should return a
            response contianing a list of users ordered by pk.
        test_post_with_valid_data: `POST` requests should create User and
            associated profile.
        test_post_with_valid_json: `POST` requests should create User and
            associated profile.
        test_post_with_invalid_data: `POST1 requests with invalid data should
            return appropriate error message.
        test_get_with_pk: `GET` requests with `pk` should return details of
            specified user.
        test_get_with_invalid_pk: `GET` requests with invalid pk should return
            appropriate error message.
        test_put_with_valid_data: `PUT` requests should update appropriate
            field, leaving others unaffected.
        test_put_with_invalid_data: `PUT` requests with invalid data should
            fail and return appropriate error message.
        test_delete_with_staff: Staff should be allowed to delete all users
        test_delete_with_self: users should be allowed to dleete their own
            accounts
        test_delete_others_fails: Non staff should not be able to delete other
            accounts.

    References:
        * http://www.django-rest-framework.org/api-guide/viewsets/
        * http://www.django-rest-framework.org/api-guide/permissions/
        * http://www.django-rest-framework.org/api-guide/testing/

    """

    def setUp(self):
        """
        Create several users for testing.
        """
        self.users = []
        for i in range(10):
            user = User.objects.create_user(
                username='user-{}'.format(i),
                email='test{}@test.test'.format(i),
                password='password23234545'
            )
            # Create one staff member
            if i == 0:
                user.is_staff = True
            self.users.append(user)
            user.save()

        self.assertEqual(len(User.objects.all()), 10)
        self.factory = APIRequestFactory()
        self.listview = UserViewset.as_view({'get': 'list', 'post': 'create'})

    def tearDown(self):
        """
        Clean test database.
        """

        for user in User.objects.all():
            user.delete()
        self.assertEqual(len(User.objects.all()), 0)

    def test_user_list_on_get(self):
        """
        `GET` request with no pk should return list of all users ordered by
        `pk`.
        """

        request = self.factory.get(reverse('user-list'))
        response = self.listview(request)
        self.assertEqual(response.status_code, 200)

        data = response.data
        users = data['results']
        self.assertEqual(data['count'], len(self.users))

        for i in range(len(self.users)):
            self.assertEqual(self.users[i].username, users[i]['username'])
            self.assertEqual(users[i]['id'], i + 1)

    def test_post_with_valid_data(self):
        """
        `POST` requests to listview should create new user object if data is
        valid.
        """
        post_data = {
            'username': 'user-11',
            'email': 'test11@test.test',
            'password': 'rubytuesday'
        }
        url = reverse('user-list')
        request = self.factory.post(url, post_data)
        response = self.listview(request)

        self.assertEqual(response.status_code, 201)

        return_data = response.data
        for key, value in post_data.items():
            if key == 'password':
                continue
            self.assertEqual(return_data[key], value)

        user = User.objects.get(id=len(self.users) + 1)

        detail_url = reverse('user-detail', args=[user.id])
        detail_url = 'http://testserver' + detail_url
        self.assertEqual(return_data['url'], detail_url)
        self.assertEqual(return_data['id'], user.id)
        self.assertEqual(return_data['email'], user.email)
        self.assertEqual(return_data['username'], user.username)

        self.assertEqual(len(self.users) + 1, len(User.objects.all()))

    def test_post_with_valid_json(self):
        """
        `POST` requests to listview should create new user object if data is
        valid.
        """
        post_data = {
            'username': 'user-11',
            'email': 'test11@test.test',
            'password': 'rubytuesday'
        }
        url = reverse('user-list')
        request = self.factory.post(url, post_data, format='json')
        response = self.listview(request)

        self.assertEqual(response.status_code, 201)

        return_data = response.data
        for key, value in post_data.items():
            if key == 'password':
                continue
            self.assertEqual(return_data[key], value)

        user = User.objects.get(id=len(self.users) + 1)

        detail_url = reverse('user-detail', args=[user.id])
        detail_url = 'http://testserver' + detail_url
        self.assertEqual(return_data['url'], detail_url)
        self.assertEqual(return_data['id'], user.id)
        self.assertEqual(return_data['email'], user.email)
        self.assertEqual(return_data['username'], user.username)

        self.assertEqual(len(self.users) + 1, len(User.objects.all()))

    def test_post_with_invalid_data(self):
        """
        `POST` should reject invalid data and return appropriate error code.
        """

        invalid_email = {
            'username': 'username',
            'email': 'notanemail',
            'password': 'password',
        }
        request = self.factory.post(reverse('user-list'), invalid_email)
        response = self.listview(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'],
                         ['Enter a valid email address.'])

        missing_username = {
            'email': 'email@e.mail',
            'password': 'password',
        }

        request = self.factory.post(reverse('user-list'), missing_username)
        response = self.listview(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('username', response.data)
        self.assertEqual(response.data['username'],
                         ['This field is required.'])

        missing_password = {
            'username': 'username',
        }

        request = self.factory.post(reverse('user-list'), missing_password)
        response = self.listview(request)
        self.assertEqual(response.status_code, 400)
        self.assertIn('password', response.data)
        self.assertEqual(response.data['password'],
                         ['This field is required.'])
