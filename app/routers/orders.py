from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Response
from sqlalchemy.orm import Session
from typing import List, Dict
import hashlib
import requests
from urllib.parse import urlencode
from app.database import get_db
from app.models import Order, OrderItem, CartItem, Product, User
from app.schemas import OrderCreate, OrderResponse
from app.auth.utils import get_current_active_user
from app.config import settings

router = APIRouter()

def generate_payfast_signature(data: Dict[str, str], passphrase: str) -> str:
    data_string = urlencode(data)
    if passphrase:
        data_string += f"&passphrase={passphrase}"
    return hashlib.md5(data_string.encode()).hexdigest()

def update_product_stock(db: Session, order_items: List[OrderItem]):
    for item in order_items:
        product = item.product
        product.stock -= item.quantity
        db.add(product)
    db.commit()

@router.post("/checkout", response_model=OrderResponse)
async def checkout(
    order_data: OrderCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Get cart items
    cart_items = db.query(CartItem).filter(
        CartItem.user_id == current_user.id
    ).all()
    
    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )
    
    # Calculate total amount
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    
    # Create order
    order = Order(
        user_id=current_user.id,
        total_amount=total_amount,
        status="pending",
        shipping_address=order_data.shipping_address.dict(),
        payment_details={
            "payment_method": order_data.payment_method
        }
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    # Create order items
    order_items = []
    for cart_item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
        order_items.append(order_item)
        db.add(order_item)
    
    # Clear cart
    for item in cart_items:
        db.delete(item)
    
    db.commit()
    
    # Prepare Payfast payment data
    payment_data = {
        # Merchant details
        "merchant_id": settings.PAYFAST_MERCHANT_ID,
        "merchant_key": settings.PAYFAST_MERCHANT_KEY,
        "return_url": f"https://your-domain.com/payment/success",
        "cancel_url": f"https://your-domain.com/payment/cancel",
        "notify_url": f"https://your-domain.com/api/webhook/payfast",
        
        # Transaction details
        "m_payment_id": str(order.id),
        "amount": f"{total_amount:.2f}",
        "item_name": f"Order #{order.id}",
        
        # Customer details
        "name_first": current_user.username,
        "email_address": current_user.email,
    }
    
    # Generate signature
    payment_data["signature"] = generate_payfast_signature(payment_data, settings.PAYFAST_PASSPHRASE)
    
    # Update order with payment URL
    order.payment_details.update({
        "payment_url": f"{settings.PAYFAST_URL}/eng/process",
        "payment_data": payment_data
    })
    db.commit()
    
    # Update product stock in background
    background_tasks.add_task(update_product_stock, db, order_items)
    
    return order

@router.get("/orders", response_model=List[OrderResponse])
async def get_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    orders = db.query(Order).filter(
        Order.user_id == current_user.id
    ).order_by(Order.created_at.desc()).all()
    
    return orders

@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return order

@router.post("/webhook/payfast")
async def payfast_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Get the raw POST data
    payload = await request.form()
    data = dict(payload)
    
    # Verify the signature
    signature = data.pop("signature", None)
    calculated_signature = generate_payfast_signature(data, settings.PAYFAST_PASSPHRASE)
    
    if signature != calculated_signature:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Verify the data
    verify_url = f"{settings.PAYFAST_URL}/eng/query/validate"
    validation = requests.post(verify_url, data=payload)
    
    if validation.text != "VALID":
        raise HTTPException(status_code=400, detail="Invalid payment notification")
    
    # Process the payment
    payment_status = data.get("payment_status")
    order_id = int(data.get("m_payment_id"))
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        if payment_status == "COMPLETE":
            order.status = "completed"
            db.commit()
        elif payment_status == "CANCELLED":
            order.status = "cancelled"
            db.commit()
    
    return Response(status_code=200) # Modified on 2025-02-20 13:01:07
