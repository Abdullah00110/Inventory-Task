# items/views.py
# import logging

# logger = logging.getLogger('items')

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Item
from .serializers import ItemSerializer
from django.core.cache import cache  # Add cache import for Redis
from django.http import JsonResponse  # JsonResponse for Redis caching

class ItemCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # logger.info("POST request received for Item creation")
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # logger.debug("Item created successfully: %s", serializer.data)
            # Clear cache after creating an item
            cache.delete('items_list')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # logger.warning("Invalid data for Item creation: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemListView(APIView):
    def get(self, request):
        # logger.info("GET request received for Item list")
        # Check if cached data is available
        items = cache.get('items_list')
        
        if not items:
            items = Item.objects.all()
            serializer = ItemSerializer(items, many=True)
            cache.set('items_list', serializer.data, timeout=60*15)  # Cache for 15 minutes
            # logger.debug("Items retrieved from database and cached")
            return Response(serializer.data)
        
        # logger.debug("Items retrieved from cache")
        return Response(items)

class ItemDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # logger.info("GET request received for Item with ID: %s", pk)
        item = cache.get(f'item_{pk}')
        if not item:
            try:
                item_obj = Item.objects.get(pk=pk)
                serializer = ItemSerializer(item_obj)
                cache.set(f'item_{pk}', serializer.data, timeout=60*15)
                # logger.debug("Item retrieved from database and cached: %s", serializer.data)
                return Response(serializer.data)
            except Item.DoesNotExist:
                # logger.error("Item with ID %s not found", pk)
                return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # logger.debug("Item retrieved from cache: %s", item)
        return Response(item)

    def put(self, request, pk):
        # logger.info("PUT request received for Item with ID: %s", pk)
        try:
            item = Item.objects.get(pk=pk)
            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                cache.delete(f'item_{pk}')
                cache.delete('items_list')
                # logger.debug("Item updated successfully: %s", serializer.data)
                return Response(serializer.data)
            # logger.warning("Invalid data for Item update: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Item.DoesNotExist:
            # logger.error("Item with ID %s not found for update", pk)
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        # logger.info("DELETE request received for Item with ID: %s", pk)
        try:
            item = Item.objects.get(pk=pk)
            item.delete()
            cache.delete(f'item_{pk}')
            cache.delete('items_list')
            # logger.debug("Item with ID %s deleted successfully", pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Item.DoesNotExist:
            # logger.error("Item with ID %s not found for deletion", pk)
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

# Redis test view
def my_view(request):
    # logger.info("GET request received for my_view")
    data = cache.get('my_key')
    if not data:
        data = {'key': 'value'}
        cache.set('my_key', data, timeout=60*15)
        # logger.debug("Data generated and cached for my_view")
    return JsonResponse(data)
