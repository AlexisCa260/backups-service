from typing import Optional

import jwt
from fastapi import Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError, InvalidTokenError

from config import JWT_ALGORITHM, SECRET_KEY

bearer_scheme = HTTPBearer(auto_error=False)


def validate_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    token: Optional[str] = Query(default=None),
) -> dict:
    if credentials and credentials.credentials:
        token_value = credentials.credentials
    elif token:
        token_value = token
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falta token de autenticación",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = validate_token(token_value)
    return payload
