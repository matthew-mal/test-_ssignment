from rest_framework.permissions import BasePermission, SAFE_METHODS
# from .models import Comment
#
#
# class IsAuthorOrNewsOwnerOrAdmin(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if isinstance(obj, Comment):
#             return (
#                     request.user == obj.author or
#                     request.user == obj.news.owner or
#                     request.user.is_staff
#             )
#         return False


class IsOwnerOrStaffOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and (obj.owner == request.user or request.user.is_staff)
        )
