from django.urls import path
from orders_app.api.views import (
    OrderViewSet,
    OrderCountView,
    CompletedOrderCountView
)

urlpatterns = [
    path('orders/', OrderViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='order-list'),
    path('orders/<int:pk>/', OrderViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'put': 'update',
        'delete': 'destroy'
    }), name='order-detail'),
    path(
        'order-count/<int:business_user_id>/',
        OrderCountView.as_view(),
        name='order-count'
    ),
    path(
        'completed-order-count/<int:business_user_id>/',
        CompletedOrderCountView.as_view(),
        name='completed-order-count'
    ),
]
