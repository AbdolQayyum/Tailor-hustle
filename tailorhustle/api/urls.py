from django.urls import path
from .views import *
urlpatterns = [
    path('api/post/<int:id>/', PostViewAPI.as_view(), name='post_detail_api'),
    path('api/user/<int:id>/', UserViewAPI.as_view(), name='user_detail_api'),
    path('api/user_posts/<int:id>/', UserPostsViewAPI.as_view(), name='user_detail_api'),
    ]