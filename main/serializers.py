from rest_framework import serializers
from .models import *

class mainImportantLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantLinks
        fields = ['user','heading','description','link','is_active']

class mainLatestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatestUpdates
        fields = ['user','update', 'created_at']

class mainHomeSerializer(serializers.ModelSerializer):
    importantLinks = mainImportantLinkSerializer()
    latestUpdates = mainLatestUpdateSerializer()

class mainGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Image_Gallery
        fields = '__all__'

class mainGlobalAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = globalAnnouncement
        fields = '__all__'