from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from orders_app.models import Order
from orders_app.api.serializers import OrderSerializer, OrderCreateSerializer
from orders_app.api.permissions import IsCustomerUser, IsBusinessUserAndOrderParticipant

class OrderListCreateView(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsCustomerUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(Q(customer_user=user) | Q(business_user=user))

class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT']:
            return [permissions.IsAuthenticated(), IsBusinessUserAndOrderParticipant()]
        if self.request.method == 'DELETE':
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class OrderCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, business_user_id, *args, **kwargs):
        business_user = get_object_or_404(User, id=business_user_id)
        count = Order.objects.filter(business_user=business_user, status=Order.Status.IN_PROGRESS).count()
        return Response({"order_count": count})

class CompletedOrderCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, business_user_id, *args, **kwargs):
        business_user = get_object_or_404(User, id=business_user_id)
        count = Order.objects.filter(business_user=business_user, status=Order.Status.COMPLETED).count()
        return Response({"completed_order_count": count})
