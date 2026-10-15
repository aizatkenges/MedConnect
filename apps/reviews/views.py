from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Review
from .permissions import IsReviewOwnerOrAdminOrReadOnly
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("appointment")
    serializer_class = ReviewSerializer
    permission_classes = [
        *viewsets.ModelViewSet.permission_classes,
        IsReviewOwnerOrAdminOrReadOnly,
    ]
    filterset_fields = {
        "appointment__doctor": ["exact"],
        "rating": ["exact", "gte", "lte"],
    }
    ordering_fields = ["rating", "created_at"]
    search_fields = ["comment"]
