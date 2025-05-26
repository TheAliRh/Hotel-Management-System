from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth.auth import authenticate_user, create_access_token, verify_token

router = APIRouter(prefix="/api/token", tags=["customers"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    token = create_access_token({"sub": user["username"]})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/protected")
def protected_route(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )
    return {"user": payload["sub"], "message": "You are authorized"}
