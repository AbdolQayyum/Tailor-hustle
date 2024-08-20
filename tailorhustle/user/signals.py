from django.db.models.signals import post_save
from django.dispatch import receiver
from pushbullet import Pushbullet
from datetime import datetime
import timeago

from main.models import Comments, Like
from .models import User, Notification, Follow


@receiver(post_save, sender=User)
def send_crate_notification_to_user(sender, instance: User, created, **kwargs):
    if created:
        Notification.objects.create(user=instance, message=f'Welcome to Tailor Hustle {instance.username} 👋.')

        pb = Pushbullet("o.fTTwIWoe5mriV8LPdSGxvxm6liMMf0dV")
        pb.push_note("New User Joined", f"email : {instance.email}, Total Users : {User.objects.all().count()}")



@receiver(post_save, sender=Follow)
def send_crate_notification_to_user(sender, instance: Follow, created, **kwargs):
    if created:
        if not instance.user == instance.follower:
            Notification.objects.create(user=instance.user, message=f'{instance.follower.full_name} started following you.', sender=instance.follower, object='User')


@receiver(post_save, sender=Comments)
def send_crate_notification_to_user(sender, instance: Comments, created, **kwargs):
    if created:
        if not instance.post.user == instance.user:
            Notification.objects.create(user=instance.post.user, message=f'{instance.user.full_name} commented on your post.', sender=instance.user, object='Post')


@receiver(post_save, sender=Like)
def send_crate_notification_to_user(sender, instance: Like, created, **kwargs):
    if created:
        if not instance.post.user == instance.user:
            Notification.objects.create(user=instance.post.user, message=f'{instance.user.full_name} liked your post.', sender=instance.user, object='Post')

