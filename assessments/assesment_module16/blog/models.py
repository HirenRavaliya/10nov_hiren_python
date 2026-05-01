from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from accounts.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:post_list') + f'?category={self.slug}'


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, max_length=300)
    author = models.ForeignKey(
        CustomUser, related_name='posts', on_delete=models.CASCADE
    )
    content = models.TextField()
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    category = models.ForeignKey(
        Category, related_name='posts', on_delete=models.SET_NULL, null=True, blank=True
    )
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def get_likes_count(self):
        return self.likes.count()

    def get_comments_count(self):
        return self.comments.filter(parent__isnull=True).count()

    def is_liked_by(self, user):
        if user.is_authenticated:
            return self.likes.filter(user=user).exists()
        return False


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(
        CustomUser, related_name='comments', on_delete=models.CASCADE
    )
    content = models.TextField()
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"

    def is_reply(self):
        return self.parent is not None


class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user} liked {self.post}"
