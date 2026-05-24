from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from orders_app.api.permissions import (
    IsBusinessUserAndOrderParticipant,
    IsCustomerUser
)
from orders_app.api.serializers import OrderCreateSerializer, OrderSerializer
from orders_app.models import Order


class OrderViewSet(viewsets.ModelViewSet):
    pagination_class = None
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(), IsCustomerUser()]
        if self.action in ['partial_update', 'update']:
            return [
                permissions.IsAuthenticated(),
                IsBusinessUserAndOrderParticipant()
            ]
        if self.action == 'destroy':
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(Q(customer_user=user) | Q(business_user=user))


class OrderCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, business_user_id, *args, **kwargs):
        count = get_order_count(business_user_id, Order.Status.IN_PROGRESS)
        return Response({"order_count": count})


class CompletedOrderCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, business_user_id, *args, **kwargs):
        count = get_order_count(business_user_id, Order.Status.COMPLETED)
        return Response({"completed_order_count": count})


def get_order_count(business_user_id, status):
    business_user = get_object_or_404(User, id=business_user_id)
    return Order.objects.filter(
        business_user=business_user,
        status=status
    ).count()
