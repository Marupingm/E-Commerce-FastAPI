# E-Commerce API with FastAPI

A modern E-Commerce API built with FastAPI, featuring user authentication, product management, shopping cart functionality, and secure payment processing with Stripe.

## Features

- User authentication with JWT tokens
- Product management (CRUD operations)
- Shopping cart functionality
- Order processing with Stripe integration
- Redis caching for improved performance
- Role-based access control (Admin vs. Regular users)
- MySQL database with SQLAlchemy ORM
- Alembic migrations
- Comprehensive API documentation with Swagger UI

## Prerequisites

- Python 3.8+
- MySQL
- Redis
- Stripe account for payment processing

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd e-commerce-fastapi
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:
```
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/ecommerce
SECRET_KEY=your-secret-key-for-jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
REDIS_URL=redis://localhost:6379
STRIPE_API_KEY=your-stripe-secret-key
```

5. Create the database:
```sql
CREATE DATABASE ecommerce;
```

6. Run database migrations:
```bash
alembic upgrade head
```

## Running the Application

1. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

2. Access the API documentation at:
```
http://localhost:8000/docs
```

## API Endpoints

### Authentication
- POST /api/register - User registration
- POST /api/login - User login

### Products
- GET /api/products - List all products
- POST /api/products - Add a new product (Admin only)
- PUT /api/products/{id} - Update a product (Admin only)
- DELETE /api/products/{id} - Delete a product (Admin only)

### Cart
- POST /api/cart/add - Add item to cart
- GET /api/cart - View cart
- PUT /api/cart/{item_id} - Update cart item
- DELETE /api/cart/{item_id} - Remove item from cart

### Orders
- POST /api/checkout - Process order
- GET /api/orders - View order history
- GET /api/orders/{order_id} - View specific order

## Testing

Run the test suite:
```bash
pytest
```

## Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication
- Role-based access control
- CORS middleware configured
- Stripe for secure payment processing

## Caching

Redis is used to cache frequently accessed data:
- Product listings
- Category listings
- Popular products

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 