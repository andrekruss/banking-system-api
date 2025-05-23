from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.utils.jwt import decode_jwt_token
from src.database.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    email = decode_jwt_token(token)
    user = await User.find_one({"email": email})
    return user
    
    