# Coderr Backend

Coderr is a platform connecting freelance professionals (business users) with clients (customer users). This is the backend implementation using Python, Django, and Django REST Framework.

## Features
- **Token Authentication:** Secure registration and login flow.
- **Profiles:** Automatic profile creation on signup, role-based distinction (`business` or `customer`).
- **Offers:** Businesses can create specific service packages (`basic`, `standard`, `premium`) atomically.
- **Orders:** Customers can place orders for specific packages.
- **Reviews:** Customers can review businesses.

## Tech Stack
- Python 3.12+
- Django 5.0+
- Django REST Framework
- SQLite (for development)
- pytest & pytest-django
- django-filter

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repository-url>
cd Coderr
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Linux/MacOS
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables
Create a `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 5. Apply Migrations
```bash
python manage.py migrate
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/registration/` - Register a new user.
- `POST /api/login/` - Login and get auth token.

### Profiles
- `GET/PATCH /api/profile/{id}/` - Manage specific profile.
- `GET /api/profiles/business/` - List all business profiles.
- `GET /api/profiles/customer/` - List all customer profiles.

### Offers
- `GET/POST /api/offers/` - List/Create offers.
- `GET/PATCH/DELETE /api/offers/{id}/` - Manage specific offer.
- `GET /api/offerdetails/{id}/` - Get details of an offer detail.

### Orders
- `GET/POST /api/orders/` - List/Create orders.
- `PATCH/DELETE /api/orders/{id}/` - Update/Delete orders.
- `GET /api/order-count/{id}/` - In-progress order count.
- `GET /api/completed-order-count/{id}/` - Completed order count.

### Reviews
- `GET/POST /api/reviews/` - List/Create reviews.
- `PATCH/DELETE /api/reviews/{id}/` - Update/Delete reviews.

### Base Info
- `GET /api/base-info/` - General platform stats.

## Testing
Run the comprehensive test suite utilizing pytest:
```bash
pytest
```
Code coverage is measured and written to the `htmlcov` directory.
