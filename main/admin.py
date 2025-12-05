from django.contrib import admin
from django.utils.html import format_html
from .models import *

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ContextInline(admin.StackedInline):
    model = Context
    extra = 1

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'cover_preview', 'intro', 'read_time', 'views', 'author', 'category', 'published', 'important', 'created_at',)
    list_filter = ('author', 'category', 'published',)
    search_fields = ('title','intro','author',)
    inlines = (ContextInline, CommentInline)

    def cover_preview(self, obj):
        if obj.cover:
            return format_html('<img src="{}" width="120" style="border-radius:6px"/>', obj.cover.url)
        return "Rasm mavjud emas"
    cover_preview.short_description = 'Cover preview'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'text', 'published', 'article', 'created_at',)
    list_filter = ('email', 'published', 'article',)


@admin.register(Moment)
class MomentAdmin(admin.ModelAdmin):
    list_display = ('title', 'photo_preview', 'description', 'author', 'published', 'created_at',)

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="80" style="border-radius:6px"/>', obj.photo.url)
        return "Rasm mavjud emas"
    photo_preview.short_description = 'Photo preview'

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'subject', 'message', 'seen', 'created_at',)
    list_filter = ('phone', 'email', 'seen',)
    search_fields = ('name', 'subject', 'message',)

admin.site.register(Newsletter)