from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from apps.orders.models import Order

class PaymentInitiateAPIView(APIView):
    """
    POST: Initiate a UPI payment for an order.
    Requires 'order_id'.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')
        if not order_id:
            return Response({'error': 'order_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        # Placeholder for UPI Intent generation
        # In a real scenario, this would generate a dynamic UPI link (e.g. upi://pay?pa=...)
        upi_intent_url = f"upi://pay?pa=store@upi&pn=ShivankStore&tr={order.order_number}&am={order.total_amount}&cu=INR"

        return Response({
            'order_id': order.id,
            'total_amount': order.total_amount,
            'upi_intent_url': upi_intent_url,
            'message': 'Scan or click the link to pay.'
        }, status=status.HTTP_200_OK)


class PaymentVerifyAPIView(APIView):
    """
    POST: Verify a UPI payment using the UTR number.
    Requires 'order_id' and 'utr_number'.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')
        utr_number = request.data.get('utr_number')

        if not order_id or not utr_number:
            return Response({'error': 'order_id and utr_number are required'}, status=status.HTTP_400_BAD_REQUEST)

        order = get_object_or_404(Order, id=order_id, user=request.user)

        # Update order with UTR and set payment status to received
        order.upi_transaction_id = utr_number
        order.payment_status = 'received'
        order.status = 'confirmed'
        order.save()

        return Response({
            'success': True,
            'message': 'Payment verified successfully. Order confirmed!'
        }, status=status.HTTP_200_OK)


class PaymentCODAdvanceAPIView(APIView):
    """
    POST: Submit a ₹49 COD advance UTR to confirm a COD order.
    Requires 'order_id' and 'utr_number'.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('order_id')
        utr_number = request.data.get('utr_number')

        if not order_id or not utr_number:
            return Response({'error': 'order_id and utr_number are required'}, status=status.HTTP_400_BAD_REQUEST)

        order = get_object_or_404(Order, id=order_id, user=request.user)
        
        if order.payment_method != 'COD':
            return Response({'error': 'Order is not Cash on Delivery.'}, status=status.HTTP_400_BAD_REQUEST)

        # Update COD advance status
        order.upi_transaction_id = utr_number
        order.cod_advance_paid = True
        order.status = 'confirmed'
        order.save()

        return Response({
            'success': True,
            'message': 'COD Advance verified successfully. Order confirmed!'
        }, status=status.HTTP_200_OK)
