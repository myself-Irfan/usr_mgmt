from rest_framework import serializers
from .models import Post
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class RegSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user