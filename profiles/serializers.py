from rest_framework import serializers
from .models import Profile
from subscribers.models import Subscriber


class ProfileSerializer(serializers.ModelSerializer):
    """
    Used to convert Profile instances into JSON format and vice-versa.
    It includes additional fields that are not part of the Profile model but are computed based on the current user.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    subscribing_id = serializers.SerializerMethodField()
    tutorial_count = serializers.ReadOnlyField()
    subscribers_count = serializers.ReadOnlyField()
    subscribing_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        """
        Returns True if the current user is the owner of the profile, False otherwise.
        """
        request = self.context['request']
        return request.user == obj.owner

    def get_subscribing_id(self, obj):
        """
        Returns the id of the Subscription instance if the current user is subscribed to the profile owner, None otherwise.
        """
        user = self.context['request'].user
        if user.is_authenticated:
            subscribing = Subscriber.objects.filter(
                owner=user, subscribed=obj.owner
            ).first()
            print(subscribing)
            return subscribing.id if subscribing else None
        return None

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'last_online', 'name',
            'content', 'image', 'is_owner', 'subscribing_id',
            'tutorial_count', 'subscribers_count', 'subscribing_count',
        ]