from django.contrib.auth.models import User
from django.db import models


class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="news")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} commented {self.news}"


class UserNewsRelation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    comments = models.ManyToManyField(Comment)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.news.title}"
