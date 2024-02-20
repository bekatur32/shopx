from rest_framework.permissions import BasePermission
from .models import *


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_seller


class IsBuyer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_seller


# class IsWholeseller(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.is_wholeseller
