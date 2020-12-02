from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    password: str
    full_name: str
    gender: int
    address: str
    avatar: str
    email: str
    DOB: str
    phone: str
    point: int = 0


class UserUpdate(BaseModel):
    password: str
    full_name: str
    gender: int
    address: str
    avatar: str
    email: str
    DOB: str
    phone: str


class UserCreate(UserBase):
    password: str
    confirm_password: str


class UserInfo(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class ProductSearch(BaseModel):
    name: str = None
    category_id: int = None
    brand_id: int = None


class PostBase(BaseModel):
    title: str
    summary: str
    content: str
    images: str
    hot: bool
    category_news_id: int
    views: int


class Post(PostBase):
    id: int

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    username: str
    email: str
    content: str
    id_news: int


class SearchBase(BaseModel):
    customer_id: int
    keyword: str
    category_id: int
    brand_id: int


class Comment(CommentBase):
    id: int

    class Config:
        orm_mode = True
