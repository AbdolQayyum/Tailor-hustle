from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q

from user.forms import UserEditForm

# from core.models import Follow
# Create your views here.
from user.models import Follow

User = get_user_model()


class ProfileView(View):
    template_name_anon = 'user/anonymous_profile.html'
    template_name_auth = 'user/authenticated_profile.html'

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')

        try:
            user = User.objects.get(username=username)
        except Exception as e:
            return HttpResponse('<h1>This page does not exist.</h1>')

        if username == request.user.username:
            context = {'user': user}
            return render(request, self.template_name_auth, context=context)
        else:
            try:
                Follow.objects.get(user=user, follower=request.user)
                is_follows_this_user = True
            except Exception as e:
                is_follows_this_user = False

            context = {'user': user, 'is_follows_this_user': is_follows_this_user}
            return render(request, self.template_name_anon, context=context)


class ProfileEditView(View):
    template_name = 'user/profile_edit.html'
    form_class = UserEditForm

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')

        if username != request.user.username:
            return HttpResponse('<h1>This page does not exist.</h1>')

        form = self.form_class(instance=request.user)
        context = {'form': form}
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Sucessfully changed profile.')
            return redirect('edit_profile', request.user.username)
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
            context = {'form': form}
            return render(request, self.template_name, context=context)


class FollowView(View):

    def post(self, request, id):
        user = User.objects.get(id=id)
        try:
            follow = Follow.objects.get(user_id=id, follower=request.user)
            follow.delete()
        except Follow.DoesNotExist:
            Follow.objects.create(user=user, follower=request.user)

        return redirect('/user/' + user.username + '/')

# class AllProfilesView(View):
#     template_name = 'user/all_profiles.html'

#     def get(self, request, *args, **kwargs):
#         search_term = request.GET.get('query')

#         if search_term:
#             all_profiles = User.objects.filter(
#                     Q(username__contains=search_term) | Q(full_name__contains=search_term)
#                 ).exclude(
#                     username=request.user.username
#                 )
#         else:
#             all_profiles = User.objects.none()

#         context = {'all_profiles': all_profiles}
#         return render(request, self.template_name, context=context)
