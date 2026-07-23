from django.urls import path
from apps.brands import views

app_name = 'brands'

urlpatterns = [
    path('<slug:slug>/', views.brand_products, name='detail'),
]
