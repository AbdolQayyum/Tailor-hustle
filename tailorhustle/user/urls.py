from django.urls import path
from user.views import (
    ProfileView,
    ProfileEditView, FollowView,
    # AllProfilesView,
)
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('<str:username>/', login_required(ProfileView.as_view()), name='profile_view'),
    path('<str:username>/edit/', login_required(ProfileEditView.as_view()), name='edit_profile'),
    path('<int:id>/follow/', login_required(FollowView.as_view()), name='follow_view'),
    # path('profiles/',
    #     login_required(AllProfilesView.as_view()), 
    #     name='all_profiles_view'),
]
