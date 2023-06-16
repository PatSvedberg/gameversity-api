from django.db import models
from django.contrib.auth.models import User


class Tutorial(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_post_j0e5er', blank=True
    )
    language = models.CharField(max_length=255)
    engine = models.CharField(max_length=255)
    engine_version = models.CharField(max_length=255)
    theme = models.CharField(max_length=255)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'


class Step(models.Model):
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    step_description = models.TextField(blank=False)
    step_image = models.ImageField(
        upload_to='images/', blank=True
    )
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.tutorial.title} - Step {self.order}'