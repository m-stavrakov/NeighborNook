from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile
from PIL import Image

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_img']

class UserSerializer(serializers.ModelSerializer):
    # password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(write_only=True)
    profile_img = serializers.ImageField(write_only=True, required=False) 
    bio = serializers.CharField(max_length=500, required=False)
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password', 'password2', 'bio', 'profile_img']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user