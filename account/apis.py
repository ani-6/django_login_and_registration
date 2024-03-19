from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .serializers import *
from .views import *
from .processors import *


class accountLogin(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
        
class accountProfile(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):  
        user = request.user
        serializer = accountUserProfileSerializer(user) 
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class accountSettings(APIView):
    def get(self, request):
        user_profile = request.user.user_profile
        user_serializer = UserSerializer(request.user)
        profile_serializer = accountProfileDataSerializer(user_profile)
        return Response({'user': user_serializer.data, 'profile': profile_serializer.data})

    def put(self, request):
        user_profile = request.user.user_profile
        user_serializer = UserSerializer(request.user, data=request.data)
        profile_serializer = accountProfileDataSerializer(user_profile, data=request.data.get('profile'))

        user_valid = user_serializer.is_valid()
        profile_valid = profile_serializer.is_valid()

        if user_valid and profile_valid:
            user_serializer.save()
            profile_serializer.save()
            return Response({'message': 'Your profile is updated successfully'}, status=status.HTTP_200_OK)
        else:
            errors = {}
            if not user_valid:
                errors['user'] = user_serializer.errors
            if not profile_valid:
                errors['profile'] = profile_serializer.errors

            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)

class accountDeleteAvtar(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        profile.profile_pic = "Account/profile_images/default.jpg"
        profile.save()
        return Response({'message': 'Avatar deleted successfully'}, status=status.HTTP_200_OK)

class accountLogout(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class accountFeedback(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        serializer = accountFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            # Set user to the current authenticated user
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        