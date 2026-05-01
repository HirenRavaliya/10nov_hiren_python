from django.contrib import admin
from .models import Post, Category, Tag, Comment, Like


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ['author', 'content', 'created_at']
    readonly_fields = ['created_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'created_at', 'get_likes_count', 'get_comments_count']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'content', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    date_hierarchy = 'created_at'
    inlines = [CommentInline]
    actions = ['make_published', 'make_draft']

    def make_published(self, request, queryset):
        queryset.update(status='published')
        self.message_user(request, 'Selected posts have been published.')
    make_published.short_description = 'Mark selected posts as Published'

    def make_draft(self, request, queryset):
        queryset.update(status='draft')
        self.message_user(request, 'Selected posts have been set to draft.')
    make_draft.short_description = 'Mark selected posts as Draft'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at', 'parent']
    list_filter = ['created_at']
    search_fields = ['author__username', 'content', 'post__title']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'post__title']
