from django.urls import path
from apps.cart import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add/', views.add_to_cart, name='add'),

    # URL-based (cart page stepper buttons)
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove'),
    path('update/<int:item_id>/', views.update_cart, name='update'),

    # Body-based (cart drawer AJAX — item_id in POST body)
    path('update/', views.update_cart_ajax, name='update-ajax'),
    path('remove/', views.remove_cart_ajax, name='remove-ajax'),

    # Cart data & count for drawer
    path('data/', views.cart_data, name='data'),
    path('count/', views.cart_count, name='count'),

    # Coupon routes
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('remove-coupon/', views.remove_coupon, name='remove_coupon'),
]
