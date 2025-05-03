from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Path, Background


class RegisterViewTestCase(TestCase):
    def test_register_get_view(self):
        url = reverse('register')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'editor/register.html')

    def test_register_post_view(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='testuser').exists())
        user = User.objects.get(username='testuser')
        self.assertTrue(user.check_password('testpassword'))

    def test_register_post_view_invalid(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'wrongpassword',
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'editor/register.html')
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_register_redirect_authenticated_user(self):
        User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        url = reverse('register')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))


class DeleteViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.path = Path.objects.create(
            name='Test Path',
            user=self.user,
            background=Background.objects.create(name='Test Background', image='path/to/image.jpg')
        )

    def test_delete_view(self):
        url = reverse('delete_path', args=[self.path.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))
        self.assertFalse(Path.objects.filter(id=self.path.id).exists())

    def test_delete_view_invalid_path(self):
        url = reverse('delete_path', args=[999])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)

    def test_delete_view_not_owner(self):
        User.objects.create_user(username='otheruser', password='otherpassword')
        self.client.logout()
        self.client.login(username='otheruser', password='otherpassword')
        url = reverse('delete_path', args=[self.path.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)


class CreateViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_create_view_get(self):
        url = reverse('create_path')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'editor/create_path.html')

    def test_create_view_post(self):
        url = reverse('create_path')
        data = {
            'name': 'New Path',
            'background': Background.objects.create(name='Test Background', image='path/to/image.jpg').id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('edit_path', args=[1]))

    def test_create_view_post_invalid(self):
        url = reverse('create_path')
        data = {
            'name': 'bad path',
            'background': '9999'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'editor/create_path.html')
        with self.assertRaises(Path.DoesNotExist):
            Path.objects.get(name='bad path')
