from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, default='')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    website = models.URLField(blank=True, default='')

    def __str__(self):
        return self.username

    # --- Role helpers ---
    def get_role(self):
        """Returns the user's role label: Admin, Author, or Reader."""
        if self.is_staff or self.is_superuser:
            return 'Admin'
        if self.groups.filter(name='Author').exists():
            return 'Author'
        return 'Reader'

    def is_author(self):
        return self.groups.filter(name='Author').exists() or self.is_staff

    def is_reader(self):
        return not self.is_author() and not self.is_staff

    def is_admin(self):
        return self.is_staff or self.is_superuser

    # --- Stat helpers ---
    def get_followers_count(self):
        return self.followers.count()

    def get_following_count(self):
        return self.following.count()

    def get_posts_count(self):
        return self.posts.filter(status='published').count()


class Follow(models.Model):
    follower = models.ForeignKey(
        CustomUser, related_name='following', on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        CustomUser, related_name='followers', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower} follows {self.following}"
