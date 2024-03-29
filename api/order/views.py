from rest_framework import viewsets, views, generics, status
from rest_framework.response import Response
from api.book.helper import LargeResultsSetPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from apps.order.models import Order, Cart, CartItem, Wishlist
from .serializers import OrderSerializer, CartSerializer, CartItemSerializer, WishlistSerializer
from .filters import OrderFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.parsers import MultiPartParser, FormParser


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-id')
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]
    pagination_class = LargeResultsSetPagination
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    parser_classes = [MultiPartParser, FormParser]
    

    def get_queryset(self):
        return Order.objects.all().order_by('-id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WishlistViewSet(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
