from django.db import models
from django.contrib.auth.models import User


class Background(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='backgrounds/')

    def __str__(self):
        return self.name


class Path(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paths')
    background = models.ForeignKey(Background, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} (user: {self.user.username})'


class Point(models.Model):
    path = models.ForeignKey(Path, on_delete=models.CASCADE, related_name='points')
    x = models.PositiveIntegerField()
    y = models.PositiveIntegerField()
    order = models.PositiveIntegerField()

    def __str__(self):
        return f'({self.x}, {self.y})'

    class Meta:
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(fields=['path', 'order'], name='unique_order_per_path')
        ]
