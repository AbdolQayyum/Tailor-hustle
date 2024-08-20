from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class PostAdmin(admin.ModelAdmin):
    model = Post

    list_display = ('id', 'get_post_file', 'post_type', 'user', 'date_posted')

    def get_post_file(self, obj):
        return mark_safe(
            f"<img src='{obj.post_file.url}' width='50' height='50' />") if obj.post_file and obj.post_type == 'image' else ""

admin.site.register(Post, PostAdmin)
admin.site.register(Comments)
admin.site.register(Like)
admin.site.register(PostViews)