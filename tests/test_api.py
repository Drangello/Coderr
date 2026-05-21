import pytest
from django.contrib.auth.models import User
from profile_app.models import Profile
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order
from reviews_app.models import Review

@pytest.mark.django_db
class TestAuthAPI:
    def test_registration(self, api_client):
        response = api_client.post('/api/registration/', {
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'password123',
            'repeated_password': 'password123',
            'type': 'customer'
        })
        assert response.status_code == 201
        assert 'token' in response.data
        assert response.data['username'] == 'newuser'
        
        # Check profile creation
        user = User.objects.get(username='newuser')
        assert user.profile.type == 'customer'

    def test_login(self, api_client, create_customer):
        create_customer('testuser', 'password123')
        response = api_client.post('/api/login/', {
            'username': 'testuser',
            'password': 'password123'
        })
        assert response.status_code == 200
        assert 'token' in response.data

@pytest.mark.django_db
class TestProfileAPI:
    def test_get_profile(self, api_client, create_customer):
        user = create_customer('cust1', 'pass1')
        api_client.force_authenticate(user=user)
        response = api_client.get(f'/api/profile/{user.profile.id}/')
        assert response.status_code == 200
        assert response.data['username'] == 'cust1'

    def test_patch_profile(self, api_client, create_customer):
        user = create_customer('cust2', 'pass2')
        api_client.force_authenticate(user=user)
        response = api_client.patch(f'/api/profile/{user.profile.id}/', {
            'first_name': 'Test'
        })
        assert response.status_code == 200
        assert response.data['first_name'] == 'Test'

    def test_list_business_profiles(self, api_client, create_business):
        user = create_business('bus1', 'pass1')
        api_client.force_authenticate(user=user)
        response = api_client.get('/api/profiles/business/')
        assert response.status_code == 200
        assert len(response.data) >= 1

@pytest.mark.django_db
class TestOfferAPI:
    def test_create_offer_as_business(self, api_client, create_business):
        user = create_business('b1', 'pass1')
        api_client.force_authenticate(user=user)
        data = {
            "title": "Design",
            "description": "Desc",
            "details": [
                {"title": "B", "revisions": 1, "delivery_time_in_days": 1, "price": 10, "offer_type": "basic", "features": []},
                {"title": "S", "revisions": 2, "delivery_time_in_days": 2, "price": 20, "offer_type": "standard", "features": []},
                {"title": "P", "revisions": 3, "delivery_time_in_days": 3, "price": 30, "offer_type": "premium", "features": []}
            ]
        }
        response = api_client.post('/api/offers/', data, format='json')
        assert response.status_code == 201
        assert response.data['title'] == "Design"
        assert len(response.data['details']) == 3

    def test_get_offers(self, api_client):
        response = api_client.get('/api/offers/')
        assert response.status_code == 200

@pytest.mark.django_db
class TestOrderAPI:
    def test_create_order(self, api_client, create_business, create_customer):
        bus = create_business('b', 'p')
        cust = create_customer('c', 'p')
        offer = Offer.objects.create(user=bus, title="T", description="D")
        detail = OfferDetail.objects.create(offer=offer, title="D", delivery_time_in_days=1, price=10, offer_type="basic")
        
        api_client.force_authenticate(user=cust)
        response = api_client.post('/api/orders/', {'offer_detail_id': detail.id})
        assert response.status_code == 201
        assert response.data['status'] == 'in_progress'

@pytest.mark.django_db
class TestReviewAPI:
    def test_create_review(self, api_client, create_business, create_customer):
        bus = create_business('b', 'p')
        cust = create_customer('c', 'p')
        
        api_client.force_authenticate(user=cust)
        response = api_client.post('/api/reviews/', {
            'business_user': bus.id,
            'rating': 5,
            'description': 'Great'
        })
        assert response.status_code == 201
        assert response.data['rating'] == 5

@pytest.mark.django_db
class TestBaseInfoAPI:
    def test_base_info(self, api_client, create_business, create_customer):
        business_1 = create_business('base_bus_1', 'pass1')
        business_2 = create_business('base_bus_2', 'pass2')
        customer_1 = create_customer('base_cust_1', 'pass1')
        customer_2 = create_customer('base_cust_2', 'pass2')
        customer_3 = create_customer('base_cust_3', 'pass3')

        Offer.objects.create(user=business_1, title='Logo Design', description='Design work')
        Offer.objects.create(user=business_2, title='Web Design', description='Web work')

        Review.objects.create(
            business_user=business_1,
            reviewer=customer_1,
            rating=4,
            description='Good',
        )
        Review.objects.create(
            business_user=business_1,
            reviewer=customer_2,
            rating=4,
            description='Good again',
        )
        Review.objects.create(
            business_user=business_2,
            reviewer=customer_3,
            rating=5,
            description='Great',
        )

        response = api_client.get('/api/base-info/')

        assert response.status_code == 200
        assert response.data == {
            'review_count': 3,
            'average_rating': 4.3,
            'business_profile_count': 2,
            'offer_count': 2,
        }

    def test_base_info_without_reviews(self, api_client):
        response = api_client.get('/api/base-info/')

        assert response.status_code == 200
        assert response.data == {
            'review_count': 0,
            'average_rating': 0.0,
            'business_profile_count': 0,
            'offer_count': 0,
        }
