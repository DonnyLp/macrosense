from django.contrib.auth.models import Group, User
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for user model."""
    class Meta:
        model = User
        fields = ['url','username','email','group']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for group model."""
    class Meta:
        fields = ['url','name']
    