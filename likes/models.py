from django.db import models
from django.contrib.auth.models import User
from tutorial.models import Tutorial


class Like(models.Model):
    """
    Like model, related to 'owner' and 'tutorial'.
    'owner' is a User instance and 'post' is a Tutorial instance.
    'unique_together' makes sure a user can't like the same tutorial twice.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    tutorial = models.ForeignKey(
        Tutorial, related_name='likes', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'tutorial']

    def __str__(self):
        return f'{self.owner} {self.tutorial}'