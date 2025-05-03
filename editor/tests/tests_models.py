from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Path, Background, Point


class BackgroundModelTestCase(TestCase):
    def setUp(self):
        self.background = Background.objects.create(
            name="Mountain", image="path/to/image.jpg"
        )

    def test_str_method(self):
        self.assertEqual(str(self.background), "Mountain")

    def test_background_creation(self):
        self.assertEqual(self.background.name, "Mountain")
        self.assertEqual(self.background.image, "path/to/image.jpg")


class PathModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.background = Background.objects.create(
            name="Mountain", image="path/to/image.jpg"
        )
        self.path = Path.objects.create(
            name="Test Path", user=self.user, background=self.background
        )

    def test_str_method(self):
        self.assertEqual(str(self.path), "Test Path (user: testuser)")

    def test_path_creation(self):
        self.assertEqual(self.path.name, "Test Path")
        self.assertEqual(self.path.user.username, "testuser")
        self.assertEqual(self.path.background.name, "Mountain")

    def test_path_points_relationship(self):
        # Create points and check the relationship
        point1 = Point.objects.create(path=self.path, x=1, y=2, order=1)
        point2 = Point.objects.create(path=self.path, x=3, y=4, order=2)
        self.assertIn(point1, self.path.points.all())
        self.assertIn(point2, self.path.points.all())
        point1.delete()
        self.assertNotIn(point1, self.path.points.all())

    def test_user_delete_cascade(self):
        # Create points and check the relationship
        point1 = Point.objects.create(path=self.path, x=1, y=2, order=1)
        point2 = Point.objects.create(path=self.path, x=3, y=4, order=2)
        self.assertIn(point1, self.path.points.all())
        self.assertIn(point2, self.path.points.all())

        # Delete the user and check if path and points are deleted
        self.user.delete()
        with self.assertRaises(Path.DoesNotExist):
            Path.objects.get(id=self.path.id)
        with self.assertRaises(Point.DoesNotExist):
            Point.objects.get(id=point1.id)
        with self.assertRaises(Point.DoesNotExist):
            Point.objects.get(id=point2.id)


class PointModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.background = Background.objects.create(
            name="Mountain", image="path/to/image.jpg"
        )
        self.path = Path.objects.create(
            name="Test Path", user=self.user, background=self.background
        )
        self.path2 = Path.objects.create(
            name="Another Path", user=self.user, background=self.background
        )
        self.point1 = Point.objects.create(path=self.path, x=1, y=2, order=1)
        self.point2 = Point.objects.create(path=self.path, x=3, y=4, order=2)

    def test_str_method(self):
        self.assertEqual(str(self.point1), "(1, 2)")
        self.assertEqual(str(self.point2), "(3, 4)")

    def test_point_ordering(self):
        # Verify ordering by 'order'
        points = list(self.path.points.all())
        self.assertEqual(points[0], self.point1)
        self.assertEqual(points[1], self.point2)

    def test_unique_order_per_path(self):
        # Try creating a Point with a duplicate order and check for error
        with self.assertRaises(Exception):
            Point.objects.create(path=self.path, x=5, y=6, order=1)

    def test_different_paths(self):
        # Create a point for a different path
        point3 = Point.objects.create(path=self.path2, x=1, y=2, order=5)
        point4 = Point.objects.create(path=self.path, x=1, y=2, order=5)
        self.assertEqual(point3.path, self.path2)
        self.assertEqual(point4.path, self.path)
        self.assertNotEqual(point3, point4)
        self.assertNotEqual(point3.path, point4.path)

    def test_path_delete_cascade(self):
        # Create points and check the relationship
        self.assertIn(self.point1, self.path.points.all())
        self.assertIn(self.point2, self.path.points.all())

        # Delete the path and check if points are deleted
        self.path.delete()
        with self.assertRaises(Point.DoesNotExist):
            Point.objects.get(id=self.point1.id)
        with self.assertRaises(Point.DoesNotExist):
            Point.objects.get(id=self.point2.id)
