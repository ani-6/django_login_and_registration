from datetime import datetime

from rest_framework import permissions, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.pagination import PageNumberPagination
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

class ImageGalleryPagination(PageNumberPagination):
    page_size = 8  # Adjust the number of items per page as per your requirement
    page_size_query_param = 'page_size'
    max_page_size = 100  # You can adjust the maximum page size if needed
    # Optional: You can add this if you want to include `total_pages` as part of the response.
    def get_paginated_response(self, data):
        return Response({
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


class mainImageGallery(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            # Get the 'search' query parameter from the request
            search_query = request.GET.get('search', None)
            
            # If a search query is provided, filter based on the caption
            if search_query:
                images = Image_Gallery.objects.filter(user=user, caption__icontains=search_query)
            else:
                images = Image_Gallery.objects.filter(user=user)

            # Paginate the queryset
            paginator = ImageGalleryPagination()
            result_page = paginator.paginate_queryset(images, request)
            
            # Serialize the paginated results
            serializer = mainGallerySerializer(result_page, many=True)
            
            # Return the paginated response
            return paginator.get_paginated_response(serializer.data)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        
class mainGlobalAnnouncement(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            annon = globalAnnouncement.objects.all()
            serializer = mainGlobalAnnouncementSerializer(annon, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)       
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        