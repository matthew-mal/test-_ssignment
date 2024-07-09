from django.contrib import admin

from news.models import News, Comment, UserNewsRelation


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner', 'date_created')
    list_filter = ('date_created', 'owner')
    search_fields = ('title', 'owner', 'content')
    date_hierarchy = 'date_created'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('news', 'author', 'content', 'created_at')
    list_filter = ('created_at', 'news')
    search_fields = ('author', 'content', 'news')
    date_hierarchy = 'created_at'


@admin.register(UserNewsRelation)
class UserNewsRelationAdmin(admin.ModelAdmin):
    pass
