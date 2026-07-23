from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from apps.wishlist.models import WishlistItem
from apps.wishlist.serializers import WishlistItemSerializer
from apps.products.models.product import Product

class WishlistAPIView(generics.ListAPIView):
    """
    GET: Retrieve all wishlist items for the authenticated user.
    """
    serializer_class = WishlistItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WishlistItem.objects.filter(user=self.request.user).select_related('product')


class WishlistToggleAPIView(APIView):
    """
    POST: Toggle a product in the wishlist (adds if missing, removes if present).
    Requires 'product_id'.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=product_id, is_active=True)
        wishlist_item = WishlistItem.objects.filter(user=request.user, product=product).first()

        if wishlist_item:
            # If exists, remove it
            wishlist_item.delete()
            return Response({'message': 'Removed from wishlist', 'is_wishlisted': False}, status=status.HTTP_200_OK)
        else:
            # If not exists, add it
            WishlistItem.objects.create(user=request.user, product=product)
            return Response({'message': 'Added to wishlist', 'is_wishlisted': True}, status=status.HTTP_201_CREATED)
