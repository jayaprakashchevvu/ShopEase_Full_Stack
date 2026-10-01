from database import SessionLocal
from modules import Category, Product

CATEGORIES = [
    ("Electronics", "https://images.unsplash.com/photo-1498049794561-7780e7231661"),
    ("Fashion", "https://images.unsplash.com/photo-1445205170230-053b83016050"),
    ("Shoes", "https://images.unsplash.com/photo-1542291026-7eec264c27ff"),
    ("Beauty", "https://images.unsplash.com/photo-1596462502278-27bfdc403348"),
    ("Home", "https://images.unsplash.com/photo-1555041469-a586c61ea9bc"),
    ("Sports", "https://images.unsplash.com/photo-1461896836934-ffe607ba8211"),
    ("Grocery", "https://images.unsplash.com/photo-1542838132-92c53300491e"),
    ("Books", "https://images.unsplash.com/photo-1544947950-fa07a98d237f"),
    ("Accessories", "https://images.unsplash.com/photo-1523275335684-37898b6baf30"),
    ("Kitchen", "https://images.unsplash.com/photo-1556911220-e15b29be8c8f"),
]

PRODUCTS = [
    ("Apple iPhone 15", "Advanced smartphone with a powerful camera system.", 69999, "Electronics", "https://images.unsplash.com/photo-1592899677977-9c10ca588bbd"),
    ("MacBook Air M2", "Lightweight laptop powered by the Apple M2 chip.", 99999, "Electronics", "https://images.unsplash.com/photo-1517336714739-489689fd1ca8"),
    ("Sony Wireless Headphones", "Comfortable wireless headphones with immersive sound.", 8999, "Electronics", "https://images.unsplash.com/photo-1505740420928-5e560c06d30e"),
    ("Classic Cotton T-Shirt", "Comfortable everyday cotton T-shirt.", 799, "Fashion", "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab"),
    ("Men's Denim Jeans", "Classic slim-fit denim jeans for everyday wear.", 1499, "Fashion", "https://images.unsplash.com/photo-1542272604-787c3835535d"),
    ("Nike Running Shoes", "Lightweight running shoes for everyday training.", 4999, "Shoes", "https://images.unsplash.com/photo-1542291026-7eec264c27ff"),
    ("Face Moisturizer", "Daily moisturizer designed to keep skin hydrated.", 599, "Beauty", "https://images.unsplash.com/photo-1556229010-6c3f2c9ca5f8"),
    ("Modern Sofa", "Comfortable modern sofa for living rooms.", 24999, "Home", "https://images.unsplash.com/photo-1555041469-a586c61ea9bc"),
    ("Professional Football", "High-quality football for training and matches.", 999, "Sports", "https://images.unsplash.com/photo-1579952363873-27f3bade9f55"),
    ("Basmati Rice 5kg", "Premium long-grain basmati rice.", 699, "Grocery", "https://images.unsplash.com/photo-1586201375761-83865001e31c"),
    ("Python Programming", "Beginner-friendly Python programming book.", 599, "Books", "https://images.unsplash.com/photo-1515879218367-8466d910aaa4"),
    ("Classic Wrist Watch", "Elegant wrist watch for everyday use.", 2499, "Accessories", "https://images.unsplash.com/photo-1523275335684-37898b6baf30"),
    ("Electric Kettle", "Fast-boiling kettle for tea and coffee.", 1299, "Kitchen", "https://images.unsplash.com/photo-1594212699903-ec8a3eca50f5"),
]


def seed():
    db = SessionLocal()
    try:
        categories = {}
        for name, image in CATEGORIES:
            category = db.query(Category).filter(Category.name == name).first()
            if not category:
                category = Category(name=name, image=image)
                db.add(category)
                db.flush()
            categories[name] = category

        for name, description, price, category_name, image_url in PRODUCTS:
            exists = db.query(Product).filter(Product.name == name).first()
            if not exists:
                db.add(Product(
                    name=name,
                    description=description,
                    price=price,
                    category_id=categories[category_name].id,
                    image_url=image_url,
                ))

        db.commit()
        print("ShopEase sample data seeded successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
