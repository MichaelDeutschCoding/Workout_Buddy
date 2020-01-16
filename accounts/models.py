from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Location(models.Model):
    name = models.CharField(max_length=31)

    def __str__(self):
        return self.name


GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other')
]

class Profile(models.Model):
    """A usable model with a one-to-one relationship to a User object.
    This object will contain all the functionality of the app and is the
     interface for all other sports/messaging models."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='user_pics', blank=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    birthdate = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=1, null=True, blank=True, choices=GENDER_CHOICES)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


