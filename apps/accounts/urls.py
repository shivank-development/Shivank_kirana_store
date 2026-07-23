from django.urls import path
from apps.accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('address/add/', views.address_add, name='address_add'),
    path('address/<int:pk>/delete/', views.address_delete, name='address_delete'),
    path('address/<int:pk>/default/', views.address_set_default, name='address_set_default'),
]
