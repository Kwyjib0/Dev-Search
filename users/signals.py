from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings #so do not have to manually enter sender email
from django.contrib.auth.models import User
from .models import Profile

# @receiver(post_save, sender=User)
# checks if profile for user has been created and if not creates one
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name
        )

        subject = 'Welcome to DevSearch'
        message = 'We are glad you have chosen to join DevSearch!'
        # trigger a verification email when profile is created
        send_mail(
            subject,
            message,
            # from email, sender
            settings.EMAIL_HOST_USER,
            # recipient, can enter multiple email addresses, must be in brackets
            [profile.email],
            # argument controls how the backend should handle errors
            fail_silently=False,        
        )


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


# @receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    user=instance.user
    user.delete()

# ALTERNATIVE TO USING DECARATORS:
# when user is saved, createProfile function is run
post_save.connect(createProfile, sender=User)
# when profile is edited, updateUser function is run
post_save.connect(updateUser, sender=Profile)
# when profile is deleted, deleteUser function is run
post_delete.connect(deleteUser, sender=Profile)
