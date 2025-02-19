from pydantic import BaseModel, EmailStr, constr, confloat, conint
from typing import Optional, List, Dict
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: constr(min_length=3, max_length=50)

class UserCreate(UserBase):
    password: constr(min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

# Product schemas
class ProductBase(BaseModel):
    name: constr(min_length=1, max_length=100)
    description: constr(max_length=500)
    price: confloat(gt=0)
    stock: conint(ge=0)
    image_url: str

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Cart schemas
class CartItemCreate(BaseModel):
    product_id: int
    quantity: conint(gt=0)

class CartItemResponse(BaseModel):
    id: int
    product: ProductResponse
    quantity: int
    created_at: datetime

    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    items: List[CartItemResponse]
    total: float

# Order schemas
class ShippingAddress(BaseModel):
    street: str
    city: str
    state: str
    country: str
    postal_code: str

class OrderCreate(BaseModel):
    shipping_address: ShippingAddress
    payment_method: str

class OrderItemResponse(BaseModel):
    id: int
    product: ProductResponse
    quantity: int
    price: float

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    items: List[OrderItemResponse]
    total_amount: float
    status: str
    shipping_address: Dict
    payment_details: Dict
    created_at: datetime

    class Config:
        from_attributes = True 