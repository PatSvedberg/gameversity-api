from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    This model represents the profile of a user. Each user has one profile.
    """
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_online = models.DateTimeField(auto_now=True)
    name  = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_profile_etwhtk'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"

def create_profile(sender, instance, created, **kwargs):
    """
    This function is a signal receiver that creates a Profile instance
    for each newly created User instance.
    """
    if created:
        Profile.objects.create(owner=instance)

post_save.connect(create_profile, sender=User)