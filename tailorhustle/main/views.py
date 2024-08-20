import timeago
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User

from user.models import Notification
from .forms import NewCommentForm, NewPostForm, NewPostFormBrand
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comments, Like, PostViews
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json
import random
from itertools import chain


class HomeView(View):
    template = 'feed.html'

    def get(self, request):
        payload = {
            'title': "Home | TailorHustle"
        }
        return render(request, self.template, payload)


class StoreDashboardView(View):
    template = 'dashboard/dashboard_stats.html'

    def get(self, request):
        posts_views = list(request.user.postviews_set.all().values_list('id', flat=True))
        posts_comments = list(Comments.objects.filter(post__user=request.user).values_list('id', flat=True))
        payload = {
            'title': "StoreDashboard | TailorHustle",
            'posts_views': posts_views,
            'posts_views_min': min(posts_views),
            'posts_views_max': max(posts_views),
            'posts_comments': posts_comments,
            'posts_comments_min': min(posts_comments),
            'posts_comments_max': max(posts_comments),
        }
        return render(request, self.template, payload)


class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        """Return 7 labels for the x-axis."""
        return ["January", "February", "March", "April", "May", "June", "July"]

    def get_providers(self):
        """Return names of datasets."""
        # return ["Central", "Eastside", "Westside"]
        return ["Views", "Likes", "Comments"]

    def get_data(self):
        """Return 3 datasets to plot."""

        # dic = [[], [], []]
        # posts = Post.objects.filter(user=self.request.user).order_by('date_posted')

        return [[75, 44, 92, 11, 44, 95, 35],
                [41, 92, 18, 3, 73, 87, 92],
                [87, 21, 94, 3, 90, 13, 65]]


line_chart = TemplateView.as_view(template_name='dashboard/charts.html')
line_chart_json = LineChartJSONView.as_view()


# class UserDashboardView(View):
#     template = 'dashboard/user_dashboard/dashboard.html'

#     def get(self, request):
#         payload = {
#             'title': "UserDashboard | TailorHustle"
#         }
#         return render(request, self.template, payload)


# POST WORK

class PostListView(ListView):
    model = Post
    template_name = 'feed.html'
    context_object_name = 'posts'
    # ordering = ['-date_posted']
    paginate_by = 15

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(PostListView, self).get_context_data(**kwargs)
        if user.is_authenticated:
            liked = [i for i in Post.objects.all() if Like.objects.filter(user=user, post=i)]
            context['liked_post'] = liked

        # Shuffle Posts randomly
        posts = context['posts']
        shuffled_posts = list(posts)
        random.shuffle(shuffled_posts)
        context['posts'] = shuffled_posts
        # Increment views for posts
        for post in posts:
            try:
                view = PostViews.objects.get(post=post, user=user)
                view.count += 1
                view.save()
            except:
                PostViews.objects.create(post=post, user=user)

        # Get user Notifications
        context['notifictions'] = Notification.objects.filter(user=user)

        return context


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'feed/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        liked = [i for i in Post.objects.filter(user=user) if Like.objects.filter(user=self.request.user, post=i)]
        context['liked_post'] = liked
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(user=user).order_by('-date_posted')


def time_format(c_time, now=None):
    from datetime import datetime
    now = datetime.now().replace(tzinfo=None)
    timeago_time_array = timeago.format(c_time.replace(tzinfo=None), now=now).split(' ')
    if timeago_time_array[0] == 'just':
        return ' '.join(timeago_time_array)
    timeago_num = timeago_time_array[0]
    timeago_char = timeago_time_array[1][0]

    return f"{timeago_num}{timeago_char}"


class MobileNotificationsView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'feed/notifications.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(MobileNotificationsView, self).get_context_data(**kwargs)
        context['notifications'] = self.request.user.get_notifications()
        return context

    def get_queryset(self):
        return Notification.objects.all().order_by('-id')


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user
    is_liked = Like.objects.filter(user=user, post=post)
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.post = post
            data.user = user
            data.save()
            return redirect('post-detail', pk=pk)
    else:
        form = NewCommentForm()
    return render(request, 'components/templates/feed/post_detail_card.html',
                  {'post': post, 'is_liked': is_liked, 'form': form})


class PostDetailView(View):
    template_name = 'feed/post_detail.html'

    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('id')

        try:
            post_obj = Post.objects.get(pk=post_id)
            try:
                view = PostViews.objects.get(post=post_obj, user=request.user)
            except:
                view = PostViews.objects.create(post=post_obj, user=request.user)
        except Exception as e:
            return redirect(request.META.get('HTTP_REFERER'))

        try:
            Like.objects.get(user=request.user, post_id=post_id)
            liked_this_post = True
        except Exception as e:
            liked_this_post = False

        # try:
        #     SavedPost.objects.get(user=request.user, post_id=post_id)
        #     post_saved = True
        # except Exception as e:
        #     post_saved = False

        context = {
            'post': post_obj,
            'liked_this_post': liked_this_post,
            # 'post_saved': post_saved,
        }

        return render(request, self.template_name, context=context)


class PostCommentView(View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('id')
        post = Post.objects.get(pk=post_id)
        comment_text = request.POST.get('comment_text', None)
        if comment_text:
            Comments.objects.create(post=post, comment=comment_text, user=request.user)
        return redirect(request.META.get('HTTP_REFERER'))


@login_required
def create_post(request):
    user = request.user
    if request.method == "POST":
        # form = NewPostForm(request.POST, request.FILES)

        form = NewPostFormBrand(request.POST, request.FILES) if request.user.user_type == 'brand' else NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.save()
            messages.success(request, f'Posted Successfully')
            return redirect('home')
    else:
        form = NewPostFormBrand(request.POST, request.FILES) if request.user.user_type == 'brand' else NewPostForm(request.POST, request.FILES)
    return render(request, 'feed/create_post.html', {'form': form})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['description', 'post_file', 'tags']
    template_name = 'feed/create_post.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.user:
            return True
        return False


@login_required
def post_delete(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user == post.user:
        Post.objects.get(pk=pk).delete()
    return redirect('home')


@login_required
def search_posts(request):
    if request.method == 'GET':
        return render(request, "feed/search_posts.html")
    else:
        query = request.POST.get('p', None)
        object_list = []
        if query:
            object_list_tag = Post.objects.filter(tags__icontains=query)
            object_list_description = Post.objects.filter(description__icontains=query)
            object_list = list(set(chain(object_list_tag, object_list_description)))
        liked = [i for i in object_list if Like.objects.filter(user=request.user, post=i)]
        context = {
            'posts': object_list,
            'liked_post': liked
        }
        return render(request, "feed/search_posts.html", context)


@login_required
def like(request):
    post_id = request.GET.get("likeId", "")
    user = request.user
    post = Post.objects.get(pk=post_id)
    liked = False
    like = Like.objects.filter(user=user, post=post)
    if like:
        like.delete()
    else:
        liked = True
        Like.objects.create(user=user, post=post)
    resp = {
        'liked': liked
    }
    response = json.dumps(resp)
    return HttpResponse(response, content_type="application/json")


class PostLike(View):
    def post(self, request, *args, **kwargs):
        post_id = kwargs.get('id')
        post = Post.objects.get(pk=post_id)

        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
        except Exception as e:
            Like.objects.create(user=request.user, post=post)

        return redirect(request.META.get('HTTP_REFERER'))
