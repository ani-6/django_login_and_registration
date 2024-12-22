from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .views import *


class accountLogin(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        auth = request.data['authmethod']
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if auth == 'session':
            if user is not None:
                login(request, user)
                user_serializer = UserSerializer(user)
                return Response({'detail': 'Login successful','user': user_serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
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
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.AllowAny]

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

class accountChangePassword(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')

            if not check_password(old_password, user.password):
                return Response({'error': 'Old password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class accountLogout(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Check if the request is authenticated by SessionAuthentication
        if isinstance(request.user, request.user.__class__) and request.auth is None:
            # Logout for session authentication
            logout(request)
            return Response({'detail': 'Session logout successful'}, status=status.HTTP_200_OK)

        # Check if the request is authenticated by TokenAuthentication
        elif isinstance(request.auth, TokenAuthentication):
            # Logout for token authentication
            if hasattr(request.user, 'auth_token'):
                request.user.auth_token.delete()
                return Response({'detail': 'Token logout successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Token not found for user'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'error': 'Authentication type not supported'}, status=status.HTTP_400_BAD_REQUEST)
        
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
        
class CheckAuthView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user_serializer = UserSerializer(user)
        return Response({"id": user.id, "is_staff":user.is_staff, "user": user_serializer.data}, status=200) 