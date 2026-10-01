from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import Base, engine
import modules
from routers import cart, categories, home, product, users

Base.metadata.create_all(bind=engine)

Path("uploads/profile").mkdir(parents=True, exist_ok=True)

app = FastAPI(
    title="ShopEase API",
    description="REST API for the ShopEase Flutter e-commerce application.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(home.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(product.router)
app.include_router(cart.router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
