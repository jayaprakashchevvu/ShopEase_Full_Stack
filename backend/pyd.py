from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class ProductCreate(BaseModel):
    name: str = Field(min_length=3, max_length=150)
    description: str = Field(min_length=5, max_length=500)
    price: int = Field(gt=0)
    category_id: int
    image_url: str | None = None


class ProductUpdate(BaseModel):
    name: str = Field(min_length=3, max_length=150)
    description: str = Field(min_length=5, max_length=500)
    price: int = Field(gt=0)
    image_url: str | None = None


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    price: int
    category: CategoryOut
    image_url: str | None = None


class CategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    image: str | None = None


class CategoryUpdate(CategoryCreate):
    pass


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    image: str | None = None


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    profile_image: str | None = None
    is_admin: bool = False


class Token(BaseModel):
    access_token: str
    token_type: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    code: str = Field(min_length=6, max_length=6)
    new_password: str = Field(min_length=6, max_length=128)


class CartCreate(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1)


class CartUpdate(BaseModel):
    quantity: int = Field(ge=1)


class CartProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: int
    image_url: str | None = None


class CartResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    product_id: int
    quantity: int
    product: CartProductResponse
