from  datetime import datetime

import timeago
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.utils import timezone


USER_Type = [
    ('regular', 'Regular'),
    ('brand', 'Brand')
]


def time_format(c_time, now=None):
    from datetime import datetime
    now = datetime.now().replace(tzinfo=None)
    timeago_time_array = timeago.format(c_time.replace(tzinfo=None), now=now).split(' ')
    if timeago_time_array[0] == 'just':
        return ' '.join(timeago_time_array)
    timeago_num = timeago_time_array[0]
    timeago_char = timeago_time_array[1][0]

    return f"{timeago_num}{timeago_char}"


class User(AbstractUser):
    picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=32, choices=USER_Type, default='Regular')
    friends = models.ManyToManyField("User", blank=True)

    # Optional fields
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    claimed = models.BooleanField(default=False)

    # first_name = None
    # last_name = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        try:
            if self.first_name:
                self.full_name = self.first_name.title() + ' ' + self.last_name[0].title() + '.'
        except:
            pass

        super(User, self).save(*args, **kwargs)

    def user_friends(self):
        self.friends.count()

    def user_following(self):
        return Follow.objects.filter(follower=self).count()
        # return 0

    def user_followers(self):
        return Follow.objects.filter(user=self).count()
        # return 0

    def get_absolute_url(self):
        return f"/user/{self.username}/"

    def user_posts(self):
        return self.post_set.all().count()

    def get_notifications(self):
        notifications = Notification.objects.filter(user=self).order_by('-id')
        for notification in notifications:
            notification.ago = time_format(notification.created_at)
        return notifications

    def __str__(self):
        return self.email


class Follow(models.Model):
    user = models.ForeignKey(User, related_name='followed_user', on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name='follower_user', on_delete=models.CASCADE)
    followed_at = models.DateTimeField(auto_now_add=True)


class FriendRequest(models.Model):
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "From {}, to {}".format(self.from_user.username, self.to_user.username)


class Notification(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, related_name='the_user', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    sender = models.ForeignKey(User, related_name='sender_user', on_delete=models.CASCADE, null=True, blank=True)
    object = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.message}"
