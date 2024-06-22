from uuid import uuid4

from rest_framework import serializers

import base.models as baseModel
import user.models as userModel


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = userModel.Profile
        fields = ['id', 'first_name', 'last_name', 'date_joined', 'email']


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = baseModel.Type
        fields = '__all__'


class ThemeSerializer(serializers.ModelSerializer):
    type = TypeSerializer(read_only=True)

    class Meta:
        model = baseModel.Theme
        fields = '__all__'


class ProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = baseModel.Proposal
        fields = '__all__'


class DebateSerializer(serializers.ModelSerializer):
    class Meta:
        model = baseModel.Debate
        fields = '__all__'


class SingInSerializer(serializers.ModelSerializer):
    class Meta:
        model = userModel.Profile
        fields = ["first_name", "last_name", "email"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        write_only=True,
        required=True,
    )
    password = serializers.CharField(
        min_length=8,
        max_length=20,
        write_only=True,
        required=True,
    )
    token = serializers.CharField(
        max_length=1000,
        read_only=True,
    )

    def create(self, **validated_data: dict) -> None:
        user = userModel.Profile.objects.get(
            email=validated_data.get('email'),
        )
        auth, created = userModel.TokenMap.objects.get_or_create(user=user)

        if not created:
            return

        auth.token = 'token'
        return auth
