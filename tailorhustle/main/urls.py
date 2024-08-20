from .views import *
from django.urls import path, include
from . import views
from .views import PostUpdateView, PostListView, UserPostListView

urlpatterns = [
    # path('feed/', HomeView.as_view(), name='home'),
    path('store_dashboard/', StoreDashboardView.as_view(), name='store_dashboard'),
    # path('user_dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
    path('chart/', line_chart, name='line_chart'),
    path('chartJSON/', line_chart_json, name='line_chart_json'),

    # POST WORK
    path('', login_required(PostListView.as_view()), name='home'),
    path('post/new/', views.create_post, name='post-create'),
    # path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/<int:id>/', login_required(PostDetailView.as_view()), name='post_detail_view'),
    # path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('like/', views.like, name='post-like'),
    path('post_like/<int:id>/', PostLike.as_view(), name='post_like_view'),
    path('post/comment/<int:id>/', PostCommentView.as_view(), name='post_comment_view'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.post_delete, name='post-delete'),
    path('search_posts/', views.search_posts, name='search_posts'),
    path('user_posts/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('mobile_notifications/', MobileNotificationsView.as_view(), name='mobile_notifications'),

]
