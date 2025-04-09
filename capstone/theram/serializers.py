from rest_framework import serializers
from .models import User, Papers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]

class PapersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Papers
        fields = ['paper']