from datetime import timedelta, datetime
import jwt

SECRET_KEY = '7583617009a9866f288b88280716763f3ef870008f79c1b3f9a9a77660a8452b'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRES_YEAR = 3 * 365


# Create access token
def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=10)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(*, data: str):
    to_decode = data
    return jwt.decode(to_decode, SECRET_KEY, algorithm=ALGORITHM)
