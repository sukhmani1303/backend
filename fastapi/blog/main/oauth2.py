from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from main import tokenlib


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return tokenlib.verify(token,credentials_exception)

    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user