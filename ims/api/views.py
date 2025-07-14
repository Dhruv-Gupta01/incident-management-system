from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied

from django.contrib.auth.models import User
from .models import Profile, Incident
from .serializers import UserSerializer, ProfileSerializer, IncidentSerializer


# 🔐 Register API: Creates User + Profile
class RegisterView(APIView):
    def post(self, request):
        print("📩 Register API Called")
        user_data = request.data.get('user')
        profile_data = request.data.get('profile')

        print("Received user data:", user_data)
        print("Received profile data:", profile_data)

        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            profile_data['user'] = user.id
            profile_serializer = ProfileSerializer(data=profile_data)

            if profile_serializer.is_valid():
                profile_serializer.save()
                print("✅ User and Profile saved successfully")
                return Response({'msg': 'User registered successfully'}, status=201)
            else:
                print("❌ Profile errors:", profile_serializer.errors)
                user.delete()  # rollback
                return Response(profile_serializer.errors, status=400)
        else:
            print("❌ User errors:", user_serializer.errors)
            return Response(user_serializer.errors, status=400)


# 📄 Incident API: Authenticated user-only
class IncidentViewSet(viewsets.ModelViewSet):
    serializer_class = IncidentSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        print("🔐 PERMISSIONS CALLED")
        print("🔍 Full Request Info:")
        print("➡️ Method:", self.request.method)
        print("➡️ Path:", self.request.path)
        print("➡️ Headers:", dict(self.request.headers))
        print("➡️ Body:", self.request.body.decode('utf-8'))  # raw body
        print("➡️ Auth Header:", self.request.headers.get("Authorization"))
        return [IsAuthenticated()]

    def get_queryset(self):
        auth_header = self.request.headers.get('Authorization')
        print("🧾 GET QUERYSET CALLED")
        print("🔑 Authorization Header:", auth_header)
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            print("➡️ Extracted Token:", token)

        return Incident.objects.filter(reporter=self.request.user)

    def perform_create(self, serializer):
        auth_header = self.request.headers.get('Authorization')
        print("📝 PERFORM CREATE CALLED")
        print("🔑 Authorization Header:", auth_header)
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            print("➡️ Extracted Token:", token)

        print("Creating incident for user:", self.request.user.username)
        serializer.save(reporter=self.request.user)

    def perform_update(self, serializer):
        print("✏️ PERFORM UPDATE CALLED")
        instance = self.get_object()
        print("Current status:", instance.status)
        if instance.status == 'Closed':
            print("❌ Cannot edit a closed incident")
            raise PermissionDenied("Closed incidents cannot be edited")
        print("✅ Updating incident")
        serializer.save()

    def list(self, request, *args, **kwargs):
        print("📄 LIST INCIDENTS CALLED")
        auth_header = request.headers.get('Authorization')
        print("🔑 Authorization Header:", auth_header)
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            print("➡️ Extracted Token:", token)
        return super().list(request, *args, **kwargs)
