from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from modules import Cart, Product, User
from pyd import CartCreate, CartResponse, CartUpdate
from security import get_current_user

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.post("/", response_model=CartResponse)
def add_to_cart(
    cart: CartCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == cart.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing = (
        db.query(Cart)
        .filter(Cart.user_id == current_user.id, Cart.product_id == cart.product_id)
        .first()
    )

    if existing:
        existing.quantity += cart.quantity
        db.commit()
        db.refresh(existing)
        return existing

    new_cart = Cart(
        user_id=current_user.id,
        product_id=cart.product_id,
        quantity=cart.quantity,
    )
    db.add(new_cart)
    db.commit()
    db.refresh(new_cart)
    return new_cart


@router.get("/", response_model=list[CartResponse])
def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(Cart)
        .filter(Cart.user_id == current_user.id)
        .all()
    )


@router.put("/{cart_id}", response_model=CartResponse)
def update_cart(
    cart_id: int,
    cart: CartUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item = (
        db.query(Cart)
        .filter(Cart.id == cart_id, Cart.user_id == current_user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    item.quantity = cart.quantity
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{cart_id}")
def delete_cart_item(
    cart_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    item = (
        db.query(Cart)
        .filter(Cart.id == cart_id, Cart.user_id == current_user.id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(item)
    db.commit()
    return {"message": "Cart item deleted successfully"}
