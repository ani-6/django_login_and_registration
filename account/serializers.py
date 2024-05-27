from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    #password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name','last_name']
        read_only_fields = ('username',)

class accountProfileDataSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(max_length=None, use_url=True, required=False, allow_null=True, allow_empty_file=True)
    
    class Meta:
        model = Profile
        fields = ['profile_picture','cover_pic','gender','headline','bio']

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