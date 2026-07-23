from django.urls import path
from apps.checkout import views

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout_view, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('check-pincode/', views.check_pincode_api, name='check_pincode'),
]

