# items/urls.py
from django.urls import path
from .views import ItemCreateView, ItemListView, ItemDetailView
from .views import my_view

urlpatterns = [
    path('create/', ItemCreateView.as_view(), name='item-create'),
    path('list/', ItemListView.as_view(), name='item-list'),
    path('<int:pk>/', ItemDetailView.as_view(), name='item-detail'),  # Retrieve, Update, Delete
    path('my-view/', my_view, name='my_view'),
]
