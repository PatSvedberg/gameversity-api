from django.db.models import Count
from rest_framework import generics, permissions, filters
from gameversity_api.permissions import IsOwnerOrReadOnly
from .models import Tutorial
from .serializers import TutorialSerializer


class TutorialList(generics.ListCreateAPIView):
    """
    List tutorials or create a tutorial if logged in
    The perform_create method associates the tutorial with the logged in user.
    """
    serializer_class = TutorialSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Tutorial.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    search_fields = [
        'owner__username',
        'title',
        'language',
        'engine',
        'theme',
    ]
    ordering_fields = [
        'likes_count',
        'comments_count',
        'likes__created_at',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TutorialDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a tutorial and edit or delete it if you own it.
    """
    serializer_class = TutorialSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Tutorial.objects.annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comment', distinct=True)
    ).order_by('-created_at')