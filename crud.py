from sqlalchemy.orm import Session
import models, schemas
from passlib.context import CryptContext
from datetime import datetime
import bcrypt

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


# Verify password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# Hash password
def get_password_hash(password):
    return pwd_context.hash(password)


# Authenticate user
def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_customer(db: Session, customer: schemas.UserBase):
    hashed_password = get_password_hash(customer.password)
    customer_item = models.Customers(username=customer.username, password=str(hashed_password),
                                     full_name=customer.full_name, gender=customer.gender, address=customer.address,
                                     avatar=customer.avatar, email=customer.email, DOB=customer.DOB,
                                     phone=customer.phone, point=customer.point)
    db.add(customer_item)
    db.commit()
    db.refresh(customer_item)
    return customer_item


def update_customer(username: str, db: Session, customer: schemas.UserUpdate):
    db_customer = get_user_by_username(db, username)
    db_customer.password = get_password_hash(customer.password)
    db_customer.full_name = customer.full_name
    db_customer.gender = customer.gender
    db_customer.address = customer.address
    db_customer.avatar = customer.avatar
    db_customer.DOB = customer.DOB
    db_customer.phone = customer.phone
    db.commit()
    db.refresh(db_customer)
    return db_customer


# Get user by username
def get_user_by_username(db: Session, username: str):
    return db.query(models.Customers).filter(models.Customers.username == username).first()


# Get all users
def get_all_users(db: Session):
    return db.query(models.Customers).all()


# Get all posts
def get_all_posts(db: Session):
    return db.query(models.News).all()


# Get post by ID
def get_post_by_id(db: Session, post_id: int):
    return db.query(models.News).filter(models.News.id == post_id).first()


# Add post
def create_new_post(db: Session, post: schemas.PostBase):
    db_news = models.News(title=post.title, summary=post.summary, content=post.content, images=post.images,
                          hot=post.hot,
                          category_news_id=post.category_news_id, views=post.views)
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news


# Delete post by ID
def del_post_by_id(db: Session, post_id: int):
    post = db.query(models.News).filter(models.News.id == post_id).first()
    db.delete(post)
    db.commit()


# Update post
def update_post(db: Session, post_id: int, post_data: schemas.PostBase):
    post = db.query(models.News).filter(models.News.id == post_id).first()
    post.title = post_data.title
    post.summary = post_data.summary
    post.content = post_data.content
    post.images = post_data.images
    post.hot = post_data.hot
    post.category_news_id = post_data.category_news_id
    post.views = post_data.views
    post.updated_at = datetime.now()
    db.commit()
    db.refresh(post)
    return post


# Delete post
def delete_post(db: Session, post_id: int):
    post = db.query(models.News).filter(models.News.id == post_id).first()
    db.delete(post)
    db.commit()
    return post


# Search products
def search(db: Session, prod: schemas.ProductSearch):
    result = db.query(models.Products)
    if prod.name is not None:
        result = result.filter(models.Products.name.contains(prod.name))
    if prod.category_id is not None:
        result = result.filter(models.Products.category_id == prod.category_id)
    if prod.category_id is not None:
        result = result.filter(models.Products.brand_id == prod.brand_id)
    return result.all()


# Save search log
def save_search(db: Session, current_user: int, item: schemas.ProductSearch):
    search_item = models.SearchLog(customer_id=current_user, keyword=item.name, category_id=item.category_id,
                                   brand_id=item.brand_id)
    db.add(search_item)
    db.commit()
    db.refresh(search_item)


# Get saved search by current_user
def get_saved_search_current_user(db: Session, current_user: int):
    return db.query(models.SearchLog).filter(models.SearchLog.customer_id == current_user).all()


# Get saved search by current_user
def get_saved_search_customer_id(db: Session, customer_id: int):
    return db.query(models.SearchLog).filter(models.SearchLog.customer_id == customer_id).all()


# Get all search log
def get_all_search(db: Session):
    return db.query(models.SearchLog).all()


# Delete search by current user
def del_search_by_current_user(db: Session, current_user: int):
    search_list = db.query(models.SearchLog).filter(models.SearchLog.customer_id == current_user).all()
    db.delete(search_list)
    db.commit()
    return search_list


# Delete search by user id
def del_search_by_customer_id(db: Session, customer_id: int):
    search_list = db.query(models.SearchLog).filter(models.SearchLog.customer_id == customer_id).all()
    db.delete(search_list)
    db.commit()
    return search_list


# Get all comments
def get_all_comments(db: Session):
    return db.query(models.Comments).all()
