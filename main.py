import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
import models
import crud
import schemas
import utils
import jwt
from jwt import PyJWTError
from database import engine, SessionLocal
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# Dependency
def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authenticate")


# Get current user
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, utils.SECRET_KEY,
                             algorithms=[utils.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except PyJWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user


# Authenticate with token
@app.post("/authenticate", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(
        db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    from datetime import timedelta
    access_token_expires = timedelta(days=utils.ACCESS_TOKEN_EXPIRES_YEAR)
    from utils import create_access_token
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Create user
@app.post("/customer")
def create_customer(customer: schemas.UserBase, db: Session = Depends(get_db)):
    db_customer = crud.get_user_by_username(db, customer.username)
    if db_customer:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_customer(db, customer=customer)


# Update user
@app.put("/customer/{username}")
def update_customer(username: str, customer: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_customer = crud.update_customer(username, db, customer)
    return updated_customer


# Get user by name
@app.get("/customer/{username}")
def read_user(username: str, db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_user)):
    if current_user:
        db_user = crud.get_user_by_username(db, username)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user


@app.get("/customers")
def read_user(db: Session = Depends(get_db), current_user: schemas.UserInfo = Depends(get_current_user)):
    return crud.get_all_users(db)


@app.post("/post", response_model=schemas.Post)
async def create_new_post(post: schemas.PostBase, current_user: schemas.UserInfo = Depends(get_current_user)
                          , db: Session = Depends(get_db)):
    return crud.create_new_post(db=db, post=post)


@app.get("/post")
async def get_all_posts(current_user: schemas.UserInfo = Depends(get_current_user)
                        , db: Session = Depends(get_db)):
    return crud.get_all_posts(db=db)


@app.get("/post/{post_id}")
async def get_post_by_id(post_id, current_user: schemas.UserInfo = Depends(get_current_user)
                         , db: Session = Depends(get_db)):
    return crud.get_post_by_id(db=db, post_id=post_id)


@app.put("/post/{post_id}", response_model=schemas.Post)
async def update_post(post_id: int, post_data: schemas.PostBase,
                      current_user: schemas.UserInfo = Depends(get_current_user)
                      , db: Session = Depends(get_db)):
    updated_post = crud.update_post(db, post_id, post_data)
    return updated_post


@app.delete('/post/{post_id}', response_model=schemas.Post)
async def delete_post(post_id: int,
                      current_user: schemas.UserInfo = Depends(get_current_user)
                      , db: Session = Depends(get_db)):
    deleted_post = crud.delete_post(db, post_id)
    return deleted_post


@app.get("/comment")
async def get_all_comments(current_user: schemas.UserInfo = Depends(get_current_user)
                           , db: Session = Depends(get_db)):
    return crud.get_all_comments(db=db)


@app.post("/search")
async def search(prod: schemas.ProductSearch, current_user: schemas.UserInfo = Depends(get_current_user)
                 , db: Session = Depends(get_db)):
    crud.save_search(db, current_user.id, prod)
    return crud.search(db=db, prod=prod)


@app.get("/get_search_current")
async def get_saved_search_current_user(current_user: schemas.UserInfo = Depends(get_current_user)
                                        , db: Session = Depends(get_db)):
    return crud.get_saved_search_current_user(db=db, current_user=current_user.id)


@app.get("/search/{customer_id}")
async def get_saved_search_customer_id(customer_id: int, current_user: schemas.UserInfo = Depends(get_current_user)
                                       , db: Session = Depends(get_db)):
    return crud.get_saved_search_customer_id(db=db, customer_id=customer_id)


@app.get("/search")
async def get_all_search(current_user: schemas.UserInfo = Depends(get_current_user)
                         , db: Session = Depends(get_db)):
    return crud.get_all_search(db)


@app.delete("/del_search_current")
async def del_search_by_current_user(current_user: schemas.UserInfo = Depends(get_current_user)
                                     , db: Session = Depends(get_db)):
    return crud.del_search_by_current_user(db=db, current_user=current_user.id)


@app.delete("/search/{customer_id}")
async def del_search_by_customer_id(customer_id: int, current_user: schemas.UserInfo = Depends(get_current_user)
                                    , db: Session = Depends(get_db)):
    return crud.del_search_by_customer_id(db=db, customer_id=customer_id)


@app.get("/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie("Authorization", domain="localhost")
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
