from django.db.models import post_save
from django.contrib.auth.models import User
from .models import Profile

def createProfile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(personOf=instance)
        print('Profile created!')

post_save.connect(createProfile, sender=User)