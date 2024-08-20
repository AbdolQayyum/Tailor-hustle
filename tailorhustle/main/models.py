from datetime import datetime

from django.urls import reverse
from django.utils import timezone
from django.db import models
import mimetypes

from user.models import User


class Post(models.Model):
    description = models.CharField(max_length=255, blank=True)
    post_file = models.FileField(upload_to='post_image/')
    date_posted = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.CharField(max_length=100, blank=True, null=True)
    price = models.IntegerField(default=None, null=True, blank=True)
    post_type = models.CharField(max_length=255, default=None, null=True, blank=True)

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        mimetypes.init()
        type = mimetypes.guess_type(self.post_file.url)[0]
        if type:
            type = type.split('/')[0]
            self.post_type = type

        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail_view', kwargs={'pk': self.pk})

    def post_likes(self):
        return self.like_set.all().count()

    def post_comments(self):
        return self.comments_set.all().count()

    def post_views(self):
        return self.postviews_set.all().count()

    class Meta:
        ordering = ['-id']


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    comment_date = models.DateTimeField(default=timezone.now)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class PostViews(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    count = models.IntegerField(default=1)
