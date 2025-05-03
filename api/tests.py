from rest_framework.test import APIClient, APITestCase
from editor.models import Path, Background, Point
from django.contrib.auth.models import User
import rest_framework.status as status

class TokenAuthGatherTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
    
    def test_token_auth(self):
        url = '/api/auth/'
        response = self.client.post(url, {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], self.user.auth_token.key)

    def test_token_auth_invalid(self):
        url = '/api/auth/'
        response = self.client.post(url, {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)


class PathAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.background = Background.objects.create(name="Mountain", image="path/to/image.jpg")
        self.path = Path.objects.create(name="Test Path", user=self.user, background=self.background)

    def test_create_path(self):
        url = '/api/paths/'
        data = {
            'name': 'New Path',
            'background': self.background.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Path.objects.count(), 2)
        self.assertEqual(Path.objects.get(id=response.data['id']).name, 'New Path')
    
    def test_get_paths(self):
        url = '/api/paths/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Path')

    def test_delete_path(self):
        url = f'/api/paths/{self.path.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Path.objects.count(), 0)

    def test_get_path_other_user(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        url = f'/api/paths/{self.path.id}/'
        self.client.force_authenticate(user=other_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_path_invalid(self):
        url = '/api/paths/999/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_path(self):
        url = f'/api/paths/{self.path.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Path')
        self.assertEqual(response.data['background'], self.background.id)

    def test_update_path(self):
        url = f'/api/paths/{self.path.id}/'
        data = {
            'name': 'Updated Path',
            'background': self.background.id
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.path.refresh_from_db()
        self.assertEqual(self.path.name, 'Updated Path')


class PointAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.background = Background.objects.create(name="Mountain", image="path/to/image.jpg")
        self.path = Path.objects.create(name="Test Path", user=self.user, background=self.background)
        self.point = Point.objects.create(path=self.path, x=1, y=2, order=1)

    def test_create_point(self):
        url = f'/api/paths/{self.path.id}/points/'
        data = {
            'x': 3,
            'y': 4,
            'order': 2
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Point.objects.count(), 2)
        self.assertEqual(Point.objects.get(id=response.data['id']).x, 3)
        self.assertEqual(Point.objects.get(id=response.data['id']).y, 4)

    def test_get_points(self):
        url = f'/api/paths/{self.path.id}/points/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['x'], 1)
        self.assertEqual(response.data[0]['y'], 2)
    
    def test_delete_point(self):
        url = f'/api/paths/{self.path.id}/points/{self.point.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Point.objects.count(), 0)

    def test_get_point_other_user(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        url = f'/api/paths/{self.path.id}/points/{self.point.id}/'
        self.client.force_authenticate(user=other_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)