from rest_framework import serializers
from tutorial.models import Tutorial, Step
from likes.models import Like

class StepSerializer(serializers.ModelSerializer):
    """
    StepSerializer is a serializer for the Step model. It includes all fields in the model.
    """
    class Meta:
        model = Step
        fields = '__all__'

class TutorialSerializer(serializers.ModelSerializer):
    """
    TutorialSerializer is a serializer for the Tutorial model. It includes fields from the model
    as well as additional fields such as is_owner, profile_id, profile_image, like_id, likes_count, 
    comments_count, and steps.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    like_id = serializers.SerializerMethodField()
    likes_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    steps = StepSerializer(many=True, required=False)

    # Validate the size and dimensions of the image
    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px!'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px!'
            )
        return value

    # Check if the request user is the owner of the tutorial
    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    # Get the id of the like object that the request user has for the tutorial
    def get_like_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            like = Like.objects.filter(
                owner = user, tutorial = obj
            ).first()
            return like.id if like else None
        return None

    class Meta:
        model = Tutorial
        fields = [
            'id', 'owner', 'is_owner', 'profile_id',
            'profile_image', 'created_at', 'updated_at',
            'title', 'description', 'image', 'language',
            'engine', 'engine_version', 'theme',
            'like_id', 'likes_count', 'comments_count',
            'steps', 'instructions',
        ]