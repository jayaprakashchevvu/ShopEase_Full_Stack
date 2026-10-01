from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from modules import Category, Product, User
from pyd import ProductCreate, ProductResponse, ProductUpdate
from security import get_admin_user

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user),
):
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    new_product = Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get("/", response_model=list[ProductResponse])
def get_products(
    search: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    sort: str | None = None,
    order: str = "asc",
    skip: int = 0,
    limit: int = 20,
    category_id: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Product)

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if category_id is not None:
        query = query.filter(Product.category_id == category_id)

    if sort == "price":
        query = query.order_by(Product.price.desc() if order == "desc" else Product.price)
    elif sort == "name":
        query = query.order_by(Product.name.desc() if order == "desc" else Product.name)
    elif sort == "id":
        query = query.order_by(Product.id.desc() if order == "desc" else Product.id)

    return query.offset(skip).limit(limit).all()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user),
):
    existing = db.query(Product).filter(Product.id == product_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")

    for field, value in product.model_dump().items():
        setattr(existing, field, value)

    db.commit()
    db.refresh(existing)
    return existing


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_admin_user),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}
