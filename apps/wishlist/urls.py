from django.urls import path
from apps.wishlist import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.wishlist_list, name='list'),
    path('toggle/<int:product_id>/', views.toggle_wishlist, name='toggle'),
    path('count/', views.wishlist_count, name='count'),
]
