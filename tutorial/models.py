from django.db import models
from django.contrib.auth.models import User


class Tutorial(models.Model):
    """
    The Tutorial model is used to store tutorials. Each tutorial is owned by a User,
    and has an associated title, description, image, language, engine, engine version, theme, 
    and instructions.
    """
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
    instructions = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'


class Step(models.Model):
    """
    The Step model is used to store individual steps in a tutorial. Each step is associated with a tutorial,
    has a description, an image, and an order.
    """
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE, related_name='steps')
    step_description = models.TextField(blank=False)
    step_image = models.ImageField(
        upload_to='images/', blank=True
    )
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.tutorial.title} - Step {self.order}'