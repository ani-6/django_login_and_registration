from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User  = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    #password = serializers.CharField(write_only=True)
    profile_picture = serializers.SerializerMethodField()
    headline = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name','last_name','profile_picture','headline']
        read_only_fields = ('username',)

    def get_profile_picture(self, obj):
        return obj.user_profile.profile_picture.url if obj.user_profile and obj.user_profile.profile_picture else None
    
    def get_headline(self, obj):
        return obj.user_profile.headline if obj.user_profile and obj.user_profile.headline else None

class accountProfileDataSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(max_length=None, use_url=True, required=False, allow_null=True, allow_empty_file=True)
    
    class Meta:
        model = Profile
        fields = ['profile_picture','cover_picture','gender','headline','bio']

class accountUserProfileSerializer(serializers.ModelSerializer):
    user_profile = accountProfileDataSerializer()

    class Meta:
        model = User
        fields = ['username','first_name','last_name','user_profile']

class accountFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = fields = ['comment',]

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)