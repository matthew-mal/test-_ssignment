from django.db.models import Count, Case, When
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import UpdateModelMixin
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import News, UserNewsRelation, Comment
from .permissions import IsOwnerOrStaffOrReadOnly, IsAuthorOrNewsOwnerOrAdmin
from .serializers import NewsSerializer, UserNewsRelationSerializer, CommentAuthorSerializer


class NewsViewSet(ModelViewSet):
    queryset = News.objects.all().annotate(
        likes=Count(Case(When(usernewsrelation__like=True, then=1))),
        num_comments=Count('comments')
    ).select_related('owner').prefetch_related('comments').order_by('-id')
    serializer_class = NewsSerializer
    parser_classes = [JSONParser]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filterset_fields = ['owner']
    search_fields = ['title', 'owner']
    ordering_fields = ['date_created', 'owner']

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()

    def get_comments(self, obj):
        comments = Comment.objects.filter(news=obj).order_by('-id')[-10]
        request = self.context.get('request')
        return {
            "comments": CommentAuthorSerializer(comments, many=True).data,
            "all_comments_link": request.build_absolute_url(reverse('news-comments-list', kwargs={'news_id': obj.id})),
        }


class UserNewsRelationViewSet(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserNewsRelation.objects.all()
    serializer_class = UserNewsRelationSerializer
    lookup_field = 'news'

    def get_object(self):
        obj, _ = UserNewsRelation.objects.get_or_create(user=self.request.user,
                                                        news_id=self.kwargs['news'])
        return obj


class CommentViewSet(ModelViewSet):
    serializer_class = CommentAuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrNewsOwnerOrAdmin]

    def get_queryset(self):
        # news_id из URL запроса
        news_id = self.kwargs['news_pk']

        queryset = Comment.objects.filter(news_id=news_id)
        return queryset

    def perform_create(self, serializer):
        news_id = self.kwargs['news_pk']
        serializer.save(author=self.request.user, news_id=news_id)
