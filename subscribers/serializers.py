from django.db import IntegrityError
from rest_framework import serializers
from .models import Subscriber


class SubscriberSerializer(serializers.ModelSerializer):
    """
    Serializer for the Subscriber model
    Create method handles the unique constraint on 'owner' and 'subscribed'
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    subscribed_name = serializers.ReadOnlyField(source='subscribed.username')

    class Meta:
        model = Subscriber
        fields = [
            'id', 'owner', 'created_at', 'subscribed', 'subscribed_name'
        ]

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({'detail': 'possible duplicate'})