from datetime import datetime

from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *

class mainHome(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            my_date = datetime.now()
            formatted_date = my_date.strftime("%a, %Y-%m-%d")
            user_ip = request.META.get('REMOTE_ADDR')
            
            user = request.user
            important_links = ImportantLinks.objects.filter(user=user)
            latest_updates = LatestUpdates.objects.filter(user=user)

            important_links_serializer = mainImportantLinkSerializer(important_links, many=True)
            latest_updates_serializer = mainLatestUpdateSerializer(latest_updates, many=True)

            data = {
                'formatted_date' : formatted_date,
                'user_ip' : user_ip,
                'important_links': important_links_serializer.data,
                'latest_updates': latest_updates_serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        
