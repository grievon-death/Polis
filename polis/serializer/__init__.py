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
