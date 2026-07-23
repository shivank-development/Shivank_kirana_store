from django.urls import path
from apps.home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about_us, name='about-us'),
    path('privacy-policy/', views.privacy_policy, name='privacy-policy'),
    path('return-policy/', views.return_policy, name='return-policy'),
    path('shipping-policy/', views.shipping_policy, name='shipping-policy'),
    path('faqs/', views.faqs, name='faqs'),
    path('contact/', views.contact_us, name='contact-us'),
]
