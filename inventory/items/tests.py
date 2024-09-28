from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Item
from django.contrib.auth.models import MyUser

class ItemAPITests(APITestCase):

    def setUp(self):
        # Create a test user
        self.Myuser = MyUser.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        # Create a test item
        self.item = Item.objects.create(name='Test Item', description='A test item description')

    def test_create_item(self):
        """Test creating an item"""
        url = reverse('item-create')  # Ensure this matches your URL patterns
        data = {
            'name': 'New Item',
            'description': 'A new item description'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)  # One existing item + one new item
        self.assertEqual(Item.objects.get(id=response.data['id']).name, 'New Item')

    def test_list_items(self):
        """Test retrieving the list of items"""
        url = reverse('item-list')  # Ensure this matches your URL patterns
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Should return one item

    def test_retrieve_item(self):
        """Test retrieving a specific item"""
        url = reverse('item-detail', args=[self.item.id])  # Ensure you have the right URL pattern
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.item.name)

    def test_update_item(self):
        """Test updating an existing item"""
        url = reverse('item-detail', args=[self.item.id])
        data = {
            'name': 'Updated Item',
            'description': 'Updated description'
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, 'Updated Item')

    def test_delete_item(self):
        """Test deleting an item"""
        url = reverse('item-detail', args=[self.item.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)  # Item should be deleted

    def test_create_item_unauthenticated(self):
        """Test that an unauthenticated user cannot create an item"""
        self.client.logout()  # Log out the user
        url = reverse('item-create')
        data = {
            'name': 'New Item',
            'description': 'A new item description'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

