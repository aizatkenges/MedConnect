from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from apps.users.models import Role

from .models import Review


class IsReviewOwnerOrAdminOrReadOnly(BasePermission):
    def has_object_permission(
        self, request: Request, view: APIView, obj: Review
    ) -> bool:
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return (
            user.role == Role.ADMIN  # type: ignore[union-attr]
            or obj.appointment.patient_id == user.pk
        )
