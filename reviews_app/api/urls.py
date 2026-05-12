from django.urls import path
from reviews_app.api.views import ReviewListCreateView, ReviewRetrieveUpdateDestroyView

urlpatterns = [
    path('reviews/', ReviewListCreateView.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewRetrieveUpdateDestroyView.as_view(), name='review-detail'),
]
