from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from gameversity_api.permissions import IsOwnerOrReadOnly
from .models import Tutorial
from .serializers import TutorialSerializer, StepSerializer

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
        DjangoFilterBackend,
    ]
    filterset_fields = [
        'owner__subscribed__owner__profile',
        'likes__owner__profile',
        'owner__profile',
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

    def perform_update(self, serializer):
        tutorial = serializer.save()
        steps_data = self.request.data.get('steps', [])
        current_steps = tutorial.steps.all()

        # Update or create the related steps
        for step_data in steps_data:
            step_id = step_data.get('id')
            if step_id:
                step = current_steps.filter(id=step_id).first()
                if step:
                    step_serializer = StepSerializer(step, data=step_data)
                else:
                    raise serializers.ValidationError("Invalid step ID.")
            else:
                step_serializer = StepSerializer(data=step_data)

            if step_serializer.is_valid(raise_exception=True):
                step_serializer.save(tutorial=tutorial)
            else:
                raise serializers.ValidationError(step_serializer.errors)

        # Delete any removed steps
        for step in current_steps:
            if step.id not in [step_data.get('id') for step_data in steps_data]:
                step.delete()
