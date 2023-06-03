from django.contrib import admin
from .models import User, AddPost, Like, Follow, Comment

# Register your models here.
class AddPostAdmin(admin.ModelAdmin):
    list_display = ["id", "add_post", "username", "timestamp"]

class FollowAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]

class LikeAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "post"]

class CommentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "post", "content", "created_at"]
    

admin.site.register(User)
admin.site.register(AddPost, AddPostAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)

