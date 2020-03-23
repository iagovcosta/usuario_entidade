from rest_framework import serializers
from .models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('__all__')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'profile', 'documento')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.documento = profile_data.get('documento', profile.documento)
        profile.save()

        return instance