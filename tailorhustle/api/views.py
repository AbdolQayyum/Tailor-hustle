from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializer import PostSerializer, UserSerializer, CommentSerializer
from main.models import Post, Comments
from user.models import User


class PostViewAPI(APIView):
    serializer = PostSerializer

    def get(self, request, id):
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return Response({'error': "Post Doesn't exist"})
        return Response({'post': self.serializer(post).data})


class UserViewAPI(APIView):
    serializer = UserSerializer

    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({'error': "User Doesn't exist"})
        return Response({'user': self.serializer(user).data})


class UserPostsViewAPI(APIView):
    serializer = PostSerializer

    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            posts = Post.objects.filter(user=user)
        except User.DoesNotExist:
            return Response({'error': "User Doesn't exist"})

        return Response({'posts': self.serializer(posts, many=True).data})


class CommentViewAPI(APIView):
    serializer = CommentSerializer

    def post(self, request, id):
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            return Response({'error': "Post Doesn't exist"})
        comment_text = request.POST.get('comment_text', None)
        if comment_text:
            Comments.objects.create(post=post, comment=comment_text, user=request.user)