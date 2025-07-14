from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Incident

# 🔐 Serializer for User model (registration, login)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# 👤 Serializer for Profile model (extra user info)
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

# 📄 Serializer for Incident model
class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'
        read_only_fields = ['incident_id', 'reporter']
