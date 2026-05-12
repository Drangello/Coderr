import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from profile_app.models import Profile

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_customer():
    def make_customer(username, password):
        user = User.objects.create_user(username=username, password=password, email=f"{username}@example.com")
        Profile.objects.create(user=user, type=Profile.UserType.CUSTOMER)
        return user
    return make_customer

@pytest.fixture
def create_business():
    def make_business(username, password):
        user = User.objects.create_user(username=username, password=password, email=f"{username}@example.com")
        Profile.objects.create(user=user, type=Profile.UserType.BUSINESS)
        return user
    return make_business
