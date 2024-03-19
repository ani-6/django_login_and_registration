from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class accountProfileDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_pic','cover_pic','gender','headline','bio','remote_fol_id']

class accountUserProfileSerializer(serializers.ModelSerializer):
    user_profile = accountProfileDataSerializer()

    class Meta:
        model = User
        fields = ['username','first_name','last_name','user_profile']

class accountFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = fields = ['comment',]
