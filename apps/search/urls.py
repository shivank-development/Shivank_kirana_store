from django.urls import path
from apps.search import views

app_name = 'search'

urlpatterns = [
    path('', views.search_view, name='results'),
    path('api/', views.search_api, name='api'),
]
