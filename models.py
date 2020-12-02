from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Float
from database import Base

from datetime import datetime


class Customers(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    full_name = Column(String)
    gender = Column(Integer)
    address = Column(String)
    avatar = Column(String)
    email = Column(String)
    DOB = Column(String)
    phone = Column(String)
    point = Column(Integer)
    remember_token = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    status = Column(Boolean, default=True)
    api_token = Column(String, nullable=False)


class CategoryNews(Base):
    __tablename__ = "categories_news"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text)
    summary = Column(Text)
    content = Column(Text)
    images = Column(Text)
    hot = Column(Boolean)
    category_news_id = Column(Integer, ForeignKey('categories_news.id'))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    views = Column(Integer)


class Comments(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    content = Column(Text)
    id_news = Column(Integer, ForeignKey('news.id'))
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    images = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    status = Column(Boolean, default=True)


class Brands(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    country = Column(String)
    logo = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    status = Column(Boolean, default=True)


class SearchLog(Base):
    __tablename__ = "search_log"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), unique=True)
    keyword = Column(String(255))
    category_id = Column(Integer)
    brand_id = Column(Integer)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


class Products(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey('categories.id'))
    price = Column(Float)
    discount = Column(Float)
    brand_id = Column(Integer, ForeignKey('brands.id'))
    images = Column(Text)
    NSX = Column(String)
    HSD = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())
    status = Column(Boolean, default=True)
