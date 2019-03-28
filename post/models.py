from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from api2 import models as UserModel

# Create your models here.


class PostModel(models.Model):

    image = models.ImageField(null=True)
    author = models.CharField(max_length=50)
    user_id = models.ForeignKey(
        UserModel.UserModel, on_delete=models.CASCADE, null=True, related_name='post')
    content = models.TextField(null=True)
    like = models.ManyToManyField(UserModel.UserModel, null=True, blank=True,
                                  through='Like', related_name='like_to', symmetrical=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    def unlike_to(self, target):
        if self == target:
            return False

        like_info, created = Like.objects.get_or_create(
            user=self,
            post=target
        )
        like_info.save()

        return created

    def like_to(self, target):
        like_info, created = Like.objects.get_or_create(
            user=self,
            post=target
        )
        like_info.delete()

        return not created

    def get_like(self):
        return self.follows.filter(user__post=self)


class Like(models.Model):
    user = models.ForeignKey(
        UserModel.UserModel, on_delete=models.CASCADE,
        related_name='user')
    post = models.ForeignKey(
        PostModel, on_delete=models.CASCADE, related_name='post')

    def __str__(self):
        return '{} -> {}'.format(
            self.user.username,
            self.post.id
        )


class CommentModel(models.Model):

    post = models.ForeignKey(
        PostModel, on_delete=models.CASCADE, null=True, related_name='comment')
    image = models.ImageField(null=True)
    author_id = models.CharField(max_length=40, null=True)
    author_name = models.CharField(max_length=40, null=True)
    content = models.TextField(null=True)
    reply = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return self.content
