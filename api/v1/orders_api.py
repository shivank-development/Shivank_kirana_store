from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from apps.orders.models import Order
from apps.orders.serializers import OrderSerializer
from apps.cart.models import Cart
from apps.accounts.models import UserAddress

class OrderListAPIView(generics.ListAPIView):
    """
    GET: Retrieve a list of the authenticated user's past orders.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailAPIView(generics.RetrieveAPIView):
    """
    GET: Retrieve details of a specific order.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreateAPIView(APIView):
    """
    POST: Create a new order from the user's active cart.
    Requires 'address_id' and 'payment_method' (UPI or COD).
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        address_id = request.data.get('address_id')
        payment_method = request.data.get('payment_method')

        if not address_id or not payment_method:
            return Response({'error': 'address_id and payment_method are required.'}, status=status.HTTP_400_BAD_REQUEST)

        cart = get_object_or_404(Cart, user=request.user)
        if cart.item_count == 0:
            return Response({'error': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        address = get_object_or_404(UserAddress, id=address_id, user=request.user)

        # Create Order
        order = Order.objects.create(
            user=request.user,
            address=address,
            subtotal=cart.subtotal,
            delivery_charge=cart.delivery_charge,
            total_amount=cart.total,
            payment_method=payment_method,
            status='placed'
        )

        # Empty the cart
        cart.items.all().delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderTrackAPIView(APIView):
    """
    GET: Retrieve live tracking data for a specific order.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk, user=request.user)
        
        delivery_boy = order.delivery_boy
        current_lat = None
        current_lng = None
        delivery_boy_name = None

        if delivery_boy:
            delivery_boy_name = delivery_boy.full_name
            if hasattr(delivery_boy, 'delivery_agent_profile'):
                current_lat = delivery_boy.delivery_agent_profile.current_lat
                current_lng = delivery_boy.delivery_agent_profile.current_lng

        tracking_data = {
            'order_id': order.id,
            'order_number': order.order_number,
            'status': order.status,
            'delivery_boy': delivery_boy_name,
            'current_lat': current_lat,
            'current_lng': current_lng,
        }
        return Response(tracking_data, status=status.HTTP_200_OK)
