from django.urls import path
from apps.delivery import views

app_name = 'delivery'

urlpatterns = [
    path('', views.delivery_home, name='home'),
    path('track/<str:order_number>/', views.active_delivery, name='active_delivery'),
]
