from rest_framework import serializers

from main.models import *
from user.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'first_name', 'first_name', 'email', 'picture', 'user_type']


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Post
        fields = ['id', 'description', 'post_file', 'date_posted', 'tags', 'post_type', 'post_likes',
                  'post_comments', 'post_views', 'user']
        # fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    post = PostSerializer()

    class Meta:
        model = Comments

    fields = ['id', 'post', 'user', 'comment', 'comment_date']
