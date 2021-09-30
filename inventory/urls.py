from django.urls import path

from inventory import views

urlpatterns = [
    path('',
         views.inventory_list,
         name='inventory-list'),
    path('<int:pk>/',
         views.inventory_detail,
         name='inventory-detail'),
]
