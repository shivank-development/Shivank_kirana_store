from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from apps.cart.models import Cart
from django.shortcuts import get_object_or_404

class DeliveryCheckAPIView(APIView):
    """
    POST: Check if delivery is available for a given pincode or location.
    Requires 'pincode'.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pincode = request.data.get('pincode')
        if not pincode:
            return Response({'error': 'pincode is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Placeholder logic: Deliver only to specific Meerut pincodes
        valid_pincodes = ['250001', '250002', '250003', '250404']
        
        if str(pincode) in valid_pincodes:
            return Response({'available': True, 'message': 'Delivery is available in your area.'}, status=status.HTTP_200_OK)
        else:
            return Response({'available': False, 'message': 'Sorry, we do not deliver to this area yet.'}, status=status.HTTP_200_OK)


class DeliveryChargeAPIView(APIView):
    """
    POST: Calculate delivery charge based on the user's current cart subtotal.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        
        return Response({
            'subtotal': cart.subtotal,
            'delivery_charge': cart.delivery_charge,
            'free_delivery_threshold': 799,
            'message': 'Free delivery on orders above ₹799' if cart.delivery_charge > 0 else 'Eligible for Free Delivery!'
        }, status=status.HTTP_200_OK)
