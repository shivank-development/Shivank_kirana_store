from django.urls import path
from apps.orders import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='list'),
    path('<int:order_id>/', views.order_detail, name='detail'),
    path('success/<int:order_id>/', views.order_success, name='success'),
    path('track/<int:order_id>/', views.order_tracking, name='tracking'),
    path('<int:order_id>/cancel/', views.order_cancel, name='cancel'),
    path('<int:order_id>/pdf/', views.order_pdf, name='pdf'),
]
