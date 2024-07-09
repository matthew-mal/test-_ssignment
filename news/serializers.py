from rest_framework import serializers

from .models import Comment, News, UserNewsRelation


class CommentAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('author', 'content', 'created_at')
        read_only_fields = ('author', 'created_at')


class NewsSerializer(serializers.ModelSerializer):
    annotated_likes = serializers.IntegerField(read_only=True)
    owner_name = serializers.CharField(source='owner.username', default='', read_only=True)

    comments = CommentAuthorSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = ('id', 'title', 'content', 'owner_name', 'date_created', 'annotated_likes', 'comments')


class UserNewsRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNewsRelation
        fields = ('news', 'like', 'in_bookmarks')
