from datetime import datetime, timedelta
from jose import JWTError, jwt
from Router import schemas

SECRET_KEY = "ApnaSecretBhidu"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 500

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("username")
        if id is None:
            raise credentials_exception
        # token_data = schemas.TokenData(email=email)
        return id
    except JWTError:
        raise credentials_exception
