from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedDefaultRouter

from news.views import NewsViewSet, UserNewsRelationViewSet, CommentViewSet

router = SimpleRouter()

router.register(r'news', NewsViewSet, basename='books')
router.register(r'user-news-relation', UserNewsRelationViewSet)

news_router = NestedDefaultRouter(router, r'news', lookup='news')
news_router.register(r'comments', CommentViewSet, basename='news-comments')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(news_router.urls)),
]
