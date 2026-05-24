from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from profile_app.api.permissions import IsOwnerOrReadOnly
from profile_app.api.serializers import ProfileSerializer
from profile_app.models import Profile


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class BusinessProfileListView(generics.ListAPIView):
    pagination_class = None
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(type=Profile.UserType.BUSINESS)


class CustomerProfileListView(generics.ListAPIView):
    pagination_class = None
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(type=Profile.UserType.CUSTOMER)
