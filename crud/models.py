from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    """
    Class representing posts.
    """

    title = models.CharField(max_length=255)
    link = models.URLField(max_length=128)
    create = models.DateTimeField(auto_now_add=True, db_index=True)
    author = models.ForeignKey(
        User, related_name="author_created", on_delete=models.CASCADE
    )
    upvotes = models.ManyToManyField(
        User, related_name="liked_posts", editable=False, through="Upvote"
    )

    def __str__(self):
        return self.title

    @property
    def upvotes_count(self):
        return self.upvotes.count()

    def add_upvote(self, user):
        """
        Adding an upvote to the post.
        """
        if Upvote.objects.filter(Q(user__id=user.id) & Q(post=self)).exists():
            return False
        Upvote.objects.create(user=user, post=self)
        return True


class Comment(models.Model):
    """
    Class representing comments.
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class Upvote(models.Model):
    """
    Class representing user's upvotes of the posts.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
