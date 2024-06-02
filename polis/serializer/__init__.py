from rest_framework import serializers

import base.models as baseModel
import user.models as userModel


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = userModel.Profile
        fields = ['__all__']


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = baseModel.Type
        fields = ['__all__']


class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = baseModel.Theme
        fields = ['__all__']


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = baseModel.Proposal
        fields = ['__all__']


class DebateSerializer(serializers.ModelSerializer):
    class Meta:
        model = baseModel.Debate
        fields = ['__all__']


class ProfileCommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        required=True,
    )
    name = serializers.CharField(
        read_only=True,
        max_length=300,
    )
    first_name = serializers.CharField(
        write_only=True,
        required=True,
        max_length=150,
    )
    last_name = serializers.CharField(
        write_only=True,
        required=True,
        max_length=150,
    )


class CommentsSerializer(serializers.Serializer):
    _id = serializers.CharField(
        read_only=True,
        max_length=24,
    )
    user = serializers.Field(
        ProfileCommentSerializer,
        required=True,
    )
    comment = serializers.CharField(
        max_length=250,
        required=True,
    )
    sources = serializers.ListField()
    timestamp = serializers.FloatField(
        read_only=True,
    )
