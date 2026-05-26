import pytest

from django.contrib.auth.models import User
from rest_framework.test import APIClient

from profile_app.models import Profile


@pytest.fixture
def api_client():
    return APIClient()


def create_user_with_profile(username, password, user_type):
    user = User.objects.create_user(
        username=username,
        password=password,
        email=f"{username}@example.com"
    )
    Profile.objects.create(user=user, type=user_type)
    return user


@pytest.fixture
def create_customer():
    def make_customer(username, password):
        return create_user_with_profile(
            username,
            password,
            Profile.UserType.CUSTOMER
        )
    return make_customer


@pytest.fixture
def create_business():
    def make_business(username, password):
        return create_user_with_profile(
            username,
            password,
            Profile.UserType.BUSINESS
        )
    return make_business
