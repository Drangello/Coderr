<h1 align="center">Coderr REST API</h1>

<p align="center">A Django REST Framework backend for a freelance marketplace. It supports token authentication, user profiles, offers, orders, reviews, and basic platform statistics.</p>

## Setup & Run Locally

### 1. Create and activate a virtual environment
```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment variables

Create a `.env` file in the project root:
```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 4. Run database migrations
```bash
python manage.py migrate
```

### 5. Start the development server
```bash
python manage.py runserver
```

> The API will be available at `http://127.0.0.1:8000/`.

## Architecture & Apps

| App | Description |
|---|---|
| **`auth_app`** | Registration and token-based login. |
| **`profile_app`** | Customer and business profile data. |
| **`offers_app`** | Service offers with basic, standard, and premium packages. |
| **`orders_app`** | Customer orders for business offers. |
| **`reviews_app`** | Customer reviews for business users. |
| **`base_info_app`** | Public platform statistics. |

## Security & Permissions

- **Authentication:** Protected endpoints require an `Authorization: Token <key>` header.
- **Profiles:** Users can update only their own profile.
- **Offers:** Only business users can create offers.
- **Orders:** Customers create orders; involved users can access their related orders.
- **Reviews:** Customers can review business users once.

## Testing

```bash
pytest
```
