from django.urls import path
from apps.notifications import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notifications_home, name='home'),
    path('<int:notif_id>/', views.notification_detail, name='detail'),
    path('unread/', views.unread_notifications, name='unread'),
    path('<int:notif_id>/read/', views.mark_notification_read, name='mark-read'),
]
