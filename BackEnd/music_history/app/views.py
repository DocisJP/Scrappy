from rest_framework.decorators import action
from rest_framework.response import Response
from .utils import scrape_history_data, save_history_data, validate_input  
from .models import Card
from .serializers import CardSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action, permission_classes




class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all().order_by('event_date')
    serializer_class = CardSerializer
    pagination_class = PageNumberPagination
    page_size = 9

   
    @permission_classes([IsAdminUser])
    @action(detail=False, methods=['get'], url_path='scrape_and_save/(?P<input_str>[^/.]+)')
    def scrape_and_save(self, request, input_str=None):
        validated_input, error = validate_input(input_str)
        if error:
            return Response({"error": error}, status=400)
        
        data = scrape_history_data(validated_input)
        
        if data:
            save_history_data(data, validated_input)
            return Response({"message": "Data scraped and saved successfully"}, status=200)
        else:
            return Response({"error": "Failed to scrape data"}, status=500)

