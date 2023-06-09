from django.contrib.auth.models import User
from .models import Tutorial
from rest_framework import status
from rest_framework.test import APITestCase


class TutorialListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='adam', password='pass')

    def test_can_list_tutorials(self):
        adam = User.objects.get(username='adam')
        Tutorial.objects.create(owner=adam, title='a title')
        response = self.client.get('/tutorials/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        print(len(response.data))

    def test_logged_in_user_can_create_tutorial(self):
        self.client.login(username='adam', password='pass')
        response = self.client.post('/tutorials/', {'title': 'a title'})
        count = Tutorial.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_not_logged_in_cant_create_tutorial(self):
        response = self.client.post('/tutorials/', {'title': 'a title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TutorialDetailViewTests(APITestCase):
    def setUp(self):
        adam = User.objects.create_user(username='adam', password='pass')
        brian = User.objects.create_user(username='brian', password='pass')
        Tutorial.objects.create(
            owner=adam, title='a title', description='adams content'
        )
        Tutorial.objects.create(
            owner=brian, title='another title', description='brians content'
        )

    def test_can_retrieve_tutorial_using_valid_id(self):
        response = self.client.get('/tutorials/3/')
        self.assertEqual(response.data['title'], 'a title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cant_retrieve_tutorial_using_invalid_id(self):
        response = self.client.get('/tutorials/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_own_tutorial(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/tutorials/3/', {'title': 'a new title'})
        tutorial = Tutorial.objects.filter(pk=3).first()
        self.assertEqual(tutorial.title, 'a new title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cant_update_another_users_tutorial(self):
        self.client.login(username='adam', password='pass')
        response = self.client.put('/tutorials/4/', {'title': 'a new title'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)