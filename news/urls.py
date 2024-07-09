from django.urls import path, include
from rest_framework.routers import SimpleRouter

from news.views import NewsViewSet, UserNewsRelationViewSet

router = SimpleRouter()

router.register(r'news', NewsViewSet, basename='books')
# router.register(r'comments', CommentsViewSet, basename='comments')
router.register(r'news_relations', UserNewsRelationViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
