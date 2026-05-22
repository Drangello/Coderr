from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import pytest

from offers_app.models import Offer, OfferDetail
from orders_app.models import Order
from profile_app.models import Profile
from reviews_app.models import Review


def offer_details():
    return [
        detail_data("B", 1, 1, 10, "basic"),
        detail_data("S", 2, 2, 20, "standard"),
        detail_data("P", 3, 3, 30, "premium"),
    ]


def detail_data(title, revisions, days, price, offer_type):
    return {
        "title": title,
        "revisions": revisions,
        "delivery_time_in_days": days,
        "price": price,
        "offer_type": offer_type,
        "features": []
    }


def create_offer_with_details(user, title="Design"):
    offer = Offer.objects.create(user=user, title=title, description="Desc")
    for detail in offer_details():
        OfferDetail.objects.create(offer=offer, **detail)
    return offer


def create_order(customer, business, status=Order.Status.IN_PROGRESS):
    return Order.objects.create(
        customer_user=customer,
        business_user=business,
        title="Readable",
        delivery_time_in_days=1,
        price=10,
        features=[],
        offer_type="basic",
        status=status
    )


def create_review(business, reviewer, rating=4):
    return Review.objects.create(
        business_user=business,
        reviewer=reviewer,
        rating=rating,
        description='Good'
    )


def patch_order_completed(api_client, order, business):
    api_client.force_authenticate(user=business)
    patch_response = api_client.patch(f'/api/orders/{order.id}/', {
        'status': Order.Status.COMPLETED
    })
    count_response = api_client.get(
        f'/api/completed-order-count/{business.id}/'
    )
    return patch_response, count_response


def post_duplicate_review(api_client, business, reviewer):
    api_client.force_authenticate(user=reviewer)
    return api_client.post('/api/reviews/', {
        'business_user': business.id,
        'rating': 5,
        'description': 'Again'
    })


def create_base_info_data(create_business, create_customer):
    business_1 = create_business('base_bus_1', 'pass1')
    business_2 = create_business('base_bus_2', 'pass2')
    customers = [
        create_customer('base_cust_1', 'pass1'),
        create_customer('base_cust_2', 'pass2'),
        create_customer('base_cust_3', 'pass3')
    ]
    create_base_info_objects(business_1, business_2, customers)


def create_base_info_objects(business_1, business_2, customers):
    create_named_offer(business_1, 'Logo Design', 'Design work')
    create_named_offer(business_2, 'Web Design', 'Web work')
    create_review(business_1, customers[0], rating=4)
    create_review(business_1, customers[1], rating=4)
    create_review(business_2, customers[2], rating=5)


def create_named_offer(user, title, description):
    return Offer.objects.create(
        user=user,
        title=title,
        description=description
    )


def assert_base_info(response, reviews, rating, profiles, offers):
    assert response.status_code == 200
    assert response.data == {
        'review_count': reviews,
        'average_rating': rating,
        'business_profile_count': profiles,
        'offer_count': offers,
    }


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

    def test_registration_validation_errors(self, api_client, create_customer):
        create_customer('used', 'password123')
        data = {
            'username': 'newuser',
            'email': 'used@example.com',
            'password': 'password123',
            'repeated_password': 'different',
            'type': 'customer'
        }
        response = api_client.post('/api/registration/', data)
        assert response.status_code == 400

    def test_login_validation_errors(self, api_client):
        missing = api_client.post('/api/login/', {'username': 'testuser'})
        invalid = api_client.post('/api/login/', {
            'username': 'testuser',
            'password': 'bad'
        })
        assert missing.status_code == 400
        assert invalid.status_code == 400

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

    def test_patch_profile_email(self, api_client, create_customer):
        user = create_customer('cust_email', 'pass2')
        api_client.force_authenticate(user=user)
        response = api_client.patch(f'/api/profile/{user.profile.id}/', {
            'email': 'changed@example.com'
        })
        user.refresh_from_db()
        assert response.status_code == 200
        assert user.email == 'changed@example.com'

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
            "details": offer_details()
        }
        response = api_client.post('/api/offers/', data, format='json')
        assert response.status_code == 201
        assert response.data['title'] == "Design"
        assert len(response.data['details']) == 3

    def test_get_offers(self, api_client):
        response = api_client.get('/api/offers/')
        assert response.status_code == 200

    def test_offer_filters_and_detail(self, api_client, create_business):
        user = create_business('filter_bus', 'pass1')
        offer = create_offer_with_details(user, title="Filtered")
        api_client.force_authenticate(user=user)
        response = api_client.get('/api/offers/?min_price=10')
        detail = api_client.get(f'/api/offerdetails/{offer.details.first().id}/')
        assert response.status_code == 200
        assert detail.status_code == 200

    def test_patch_offer_updates_details(self, api_client, create_business):
        user = create_business('owner_bus', 'pass1')
        offer = create_offer_with_details(user)
        api_client.force_authenticate(user=user)
        data = {"title": "Updated", "details": offer_details()}
        response = api_client.patch(f'/api/offers/{offer.id}/', data, format='json')
        assert response.status_code == 200
        assert response.data['title'] == "Updated"

    def test_offer_validation_and_permissions(self, api_client, create_customer):
        user = create_customer('offer_customer', 'pass1')
        api_client.force_authenticate(user=user)
        response = api_client.post('/api/offers/', {
            "title": "Design",
            "description": "Desc",
            "details": offer_details()
        }, format='json')
        assert response.status_code == 403

@pytest.mark.django_db
class TestOrderAPI:
    def test_create_order(self, api_client, create_business, create_customer):
        bus = create_business('b', 'p')
        cust = create_customer('c', 'p')
        offer = create_offer_with_details(bus)
        detail = offer.details.first()
        api_client.force_authenticate(user=cust)
        response = api_client.post('/api/orders/', {'offer_detail_id': detail.id})
        assert response.status_code == 201
        assert response.data['status'] == 'in_progress'

    def test_order_update_counts(self, api_client, create_business, create_customer):
        bus = create_business('order_bus', 'p')
        cust = create_customer('order_cust', 'p')
        order = create_order(cust, bus)
        patch_response, count_response = patch_order_completed(
            api_client,
            order,
            bus
        )
        assert patch_response.status_code == 200
        assert count_response.data['completed_order_count'] == 1

    def test_order_list(self, api_client, create_business, create_customer):
        bus = create_business('order_list_bus', 'p')
        cust = create_customer('order_list_cust', 'p')
        create_order(cust, bus)
        api_client.force_authenticate(user=bus)
        response = api_client.get('/api/orders/')
        assert response.status_code == 200

    def test_order_create_invalid_detail(self, api_client, create_customer):
        user = create_customer('invalid_order_cust', 'p')
        api_client.force_authenticate(user=user)
        response = api_client.post('/api/orders/', {'offer_detail_id': 999})
        assert response.status_code == 400

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

    def test_dup_update_review(self, api_client, create_business, create_customer):
        bus = create_business('review_bus', 'p')
        cust = create_customer('review_cust', 'p')
        review = create_review(bus, cust)
        duplicate = post_duplicate_review(api_client, bus, cust)
        update = api_client.patch(f'/api/reviews/{review.id}/', {
            'business_user': create_business('other_bus', 'p').id,
            'rating': 3
        })
        review.refresh_from_db()
        assert duplicate.status_code == 400
        assert update.status_code == 200
        assert review.business_user == bus

    def test_permission_and_string_helpers(self, create_business, create_customer):
        bus = create_business('string_bus', 'p')
        cust = create_customer('string_cust', 'p')
        offer = create_offer_with_details(bus)
        order = create_order(cust, bus)
        review = create_review(bus, cust, rating=5)
        Token.objects.get_or_create(user=bus)
        assert str(bus.profile) == "string_bus (business)"
        assert "Design by string_bus" in str(offer)
        assert "Readable" in str(order)
        assert "string_cust" in str(review)

@pytest.mark.django_db
class TestBaseInfoAPI:
    def test_base_info(self, api_client, create_business, create_customer):
        create_base_info_data(create_business, create_customer)
        response = api_client.get('/api/base-info/')
        assert_base_info(response, 3, 4.3, 2, 2)

    def test_base_info_without_reviews(self, api_client):
        response = api_client.get('/api/base-info/')

        assert_base_info(response, 0, 0.0, 0, 0)
