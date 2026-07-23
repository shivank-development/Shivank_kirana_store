from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count
from django.utils import timezone

from api.v1.permissions import IsAdminUser
from apps.accounts.models import CustomUser
from apps.orders.models import Order
from apps.products.models.product import Product
from apps.orders.serializers import OrderSerializer
from apps.products.serializers.product_serializer import ProductSerializer


class AdminDashboardStatsAPIView(APIView):
    """
    GET: Retrieve overall dashboard statistics.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_orders = Order.objects.count()
        total_revenue = Order.objects.filter(payment_status='received').aggregate(total=Sum('total_amount'))['total'] or 0
        total_users = CustomUser.objects.count()
        pending_orders = Order.objects.filter(status='placed').count()

        return Response({
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'total_users': total_users,
            'pending_orders': pending_orders
        }, status=status.HTTP_200_OK)


class AdminOrderListAPIView(generics.ListAPIView):
    """
    GET: Retrieve all orders with filter capabilities.
    """
    permission_classes = [IsAdminUser]
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by('-placed_at')
    # Can add django-filters here for specific status filtering


class AdminOrderStatusUpdateAPIView(APIView):
    """
    PUT: Update the status of an order.
    """
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        new_status = request.data.get('status')

        if new_status not in dict(Order.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        # Handle timestamp updates if needed (e.g., delivered_at = timezone.now())
        if new_status == 'delivered':
            order.delivered_at = timezone.now()
        
        order.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)


class AdminPaymentActionAPIView(APIView):
    """
    PUT: Approve or Reject a payment manually.
    """
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        action = request.data.get('action') # 'approve' or 'reject'

        if action == 'approve':
            order.payment_status = 'received'
            order.status = 'confirmed'
        elif action == 'reject':
            order.payment_status = 'rejected'
        else:
            return Response({'error': "Action must be 'approve' or 'reject'"}, status=status.HTTP_400_BAD_REQUEST)

        order.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)


class AdminProductListCreateAPIView(generics.ListCreateAPIView):
    """
    GET: List all products
    POST: Create a new product
    """
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by('-created_at')


class AdminProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a product
    PUT/PATCH: Update a product
    DELETE: Delete a product
    """
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class AdminProductBulkImportAPIView(APIView):
    """
    POST: Bulk import products (Placeholder logic)
    """
    permission_classes = [IsAdminUser]

    def post(self, request):
        # Placeholder for processing a CSV or JSON file upload
        return Response({'message': 'Bulk import logic initiated successfully.'}, status=status.HTTP_200_OK)


class AdminRevenueAnalyticsAPIView(APIView):
    """
    GET: Retrieve revenue analytics data.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        # Placeholder for more complex grouped analytics
        total_revenue = Order.objects.filter(payment_status='received').aggregate(total=Sum('total_amount'))['total'] or 0
        return Response({
            'total_historical_revenue': total_revenue,
            'message': 'Advanced time-series analytics can be added here.'
        }, status=status.HTTP_200_OK)


class AdminLowStockAlertsAPIView(generics.ListAPIView):
    """
    GET: Retrieve products with low stock.
    """
    permission_classes = [IsAdminUser]
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        # Return active products where stock is at or below min_stock_alert threshold
        from django.db.models import F
        return Product.objects.filter(
            is_active=True,
            stock__lte=F('min_stock_alert')
        ).order_by('stock')
