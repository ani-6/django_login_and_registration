from rest_framework import serializers
from .models import *

class mainImportantLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantLinks
        fields = ['user','heading','description','link','is_active']

class mainLatestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatestUpdates
        fields = ['user','update']

class mainHomeSerializer(serializers.ModelSerializer):
    importantLinks = mainImportantLinkSerializer()
    latestUpdates = mainLatestUpdateSerializer()
