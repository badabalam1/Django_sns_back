from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class UserModel(AbstractUser):

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('not-specified', 'Not-specified')
    )

    profile_image = models.ImageField(null=True)
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    phone = models.CharField(max_length=140, null=True)
    gender = models.CharField(max_length=80, choices=GENDER_CHOICES, null=True)
    follows = models.ManyToManyField(
        'self',
        null=True,
        blank=True,
        through='Follow',
        related_name='followed_to',
        symmetrical=False
    )

    def __str__(self):
        return self.username

    def follow_to(self, target):
        if self == target:
            return False

        follow_info, created = Follow.objects.get_or_create(
            follower=self,
            following=target,
        )
        follow_info.save()

        return created

    def unfollow_to(self, target):
        follow_info, created = Follow.objects.get_or_create(
            following=target,
            follower=self,
        )
        follow_info.delete()

        return not created

    def get_followings(self):
        return self.follows.filter(followings__follower=self)

    def get_followers(self):
        return self.followed_to.filter(followers__following=self)


class Follow(models.Model):
    follower = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    following = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='followings'
    )
    followed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} -> {}'.format(
            self.follower.username,
            self.following.username,
        )
