from datetime import datetime, timedelta, timezone
from fastapi import status
from http.client import HTTPException
from jwt import ExpiredSignatureError, InvalidTokenError
import jwt
import os

def generate_jwt_token(data: dict) -> str:
    data_to_encode = data.copy()
    data_to_encode.update({"exp": datetime.now(timezone.utc) + timedelta(minutes=float(os.getenv("JWT_EXPIRATION_TIME")))})
    token = jwt.encode(data_to_encode, os.getenv("JWT_SECRET_KEY"), algorithm=os.getenv("ENCODING_ALGORITHM"))
    return token

def decode_jwt_token(encoded_token: str) -> str:
    try:
        decoded_data = jwt.decode(
            encoded_token,
            os.getenv("JWT_SECRET_KEY"),
            algorithms=[os.getenv("ENCODING_ALGORITHM")]
        )
        return decoded_data["sub"]
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired.")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")

    