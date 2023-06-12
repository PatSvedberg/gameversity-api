from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from gameversity_api.permissions import IsOwnerOrReadOnly
from .models import Profile
from .serializers import ProfileSerializer



class ProfileList(generics.ListAPIView):
    """
    List all profiles.
    No create view as profile creation is handled by django signals.
    """
    queryset = Profile.objects.annotate(
        tutorial_count=Count('owner__tutorial', distinct=True),
        subscribers_count=Count('owner__subscribed', distinct=True),
        subscribing_count=Count('owner__subscribing', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer
    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__subscribing__subscribed__profile',
        'owner__subscribed__owner__profile',
    ]
    ordering_fields = [
        'tutorial_count',
        'subscribers_count',
        'subscribing_count',
        'owner__subscribing__created_at',
        'owner__subscribed__created_at',
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.annotate(
        tutorial_count=Count('owner__tutorial', distinct=True),
        subscribers_count=Count('owner__subscribed', distinct=True),
        subscribing_count=Count('owner__subscribing', distinct=True)
    ).order_by('-created_at')
    serializer_class = ProfileSerializer