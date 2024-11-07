from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from supabase import create_client, Client
import os
import gotrue.errors

router = APIRouter()

# Supabase client setup
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Authentication setup
security = HTTPBearer()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(request: LoginRequest):
    try:
        auth_response = supabase.auth.sign_in_with_password(
            {
                "email": request.email,
                "password": request.password
            })
        if not auth_response.user or not auth_response.session:
            raise HTTPException(status_code=401, detail="Authentication failed")
    except gotrue.errors.AuthApiError:
        raise HTTPException(status_code=401, detail="Invalid login credentials")

    return JSONResponse(content={"token": auth_response.session.access_token})

@router.get("/verify")
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        user = supabase.auth.get_user(token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
    except gotrue.errors.AuthApiError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return JSONResponse(content={"status": "verified"})