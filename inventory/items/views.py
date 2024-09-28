# items/views.py

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
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Clear cache after creating an item
            cache.delete('items_list')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemListView(APIView):
    def get(self, request):
        # Check if cached data is available
        items = cache.get('items_list')
        
        if not items:
            items = Item.objects.all()
            serializer = ItemSerializer(items, many=True)
            cache.set('items_list', serializer.data, timeout=60*15)  # Cache for 15 minutes
            return Response(serializer.data)
        return Response(items)

class ItemDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        item = cache.get(f'item_{pk}')
        if not item:
            try:
                item_obj = Item.objects.get(pk=pk)
                serializer = ItemSerializer(item_obj)
                cache.set(f'item_{pk}', serializer.data, timeout=60*15)
                return Response(serializer.data)
            except Item.DoesNotExist:
                return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(item)

    def put(self, request, pk):
        try:
            item = Item.objects.get(pk=pk)
            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                cache.delete(f'item_{pk}')
                cache.delete('items_list')
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Item.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            item = Item.objects.get(pk=pk)
            item.delete()
            cache.delete(f'item_{pk}')
            cache.delete('items_list')
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Item.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

# Redis test view
def my_view(request):
    data = cache.get('my_key')
    if not data:
        data = {'key': 'value'}
        cache.set('my_key', data, timeout=60*15)
    return JsonResponse(data)
