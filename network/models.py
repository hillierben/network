from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)

    def __str__(self):
            return f"{self.username}"
    
    def id(self):
         return self.id
    
    

class AddPost(models.Model):
    add_post = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_post")

    def __str__(self):
        return f"{self.id} {self.add_post} {self.timestamp} {self.username}"
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")
    post = models.ForeignKey(AddPost, on_delete=models.CASCADE, related_name="post_post")

    def __str__(self):
            return f"{self.user} {self.post}"


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_profile")
    follows = models.ForeignKey(User,
        related_name="followed_by", 
        blank=True, 
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user} follows {self.follows}"
    
    def list(self):
         return {
              "user": self.user,
              "follower": self.follows
         }
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    post = models.ForeignKey(AddPost, on_delete=models.CASCADE, related_name="post_comment")
    content = models.TextField(max_length=800)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} {self.content} {self.user} {self.post} {self.created_at} "

