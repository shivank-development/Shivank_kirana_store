from django.urls import path
from apps.categories import views

app_name = 'categories'

urlpatterns = [
    path('<slug:slug>/', views.category_products, name='detail'),
]
