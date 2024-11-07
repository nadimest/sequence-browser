from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from supabase import create_client, Client
import os
import gotrue.errors

app = FastAPI()

# Supabase client setup
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Static files setup
app.mount("/static", StaticFiles(directory="static"), name="static")

# Authentication setup
security = HTTPBearer()

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/auth/login")
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

@app.get("/auth/verify")
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        user = supabase.auth.get_user(token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token")
    except gotrue.errors.AuthApiError:
        raise HTTPException(status_code=401, detail="Invalid token")
    return JSONResponse(content={"status": "verified"})

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    with open("templates/index.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/main_app", response_class=HTMLResponse)
async def main_app():
    with open("templates/main_app.html") as f:
        return HTMLResponse(content=f.read())

# @app.get("/data/pdb_examples", response_class=PlainTextResponse)
# async def load_pdb(credentials: HTTPAuthorizationCredentials = Depends(security)):
#     token = credentials.credentials
#     supabase.auth.session = {"access_token": token}

#     # Fetch the PDB file from Supabase storage
#     try:
#         pdb_content = supabase.storage.from_('pdb_files').download('2krh.pdb')  ## Hardcoded example
#     except Exception as e:
#         raise HTTPException(status_code=404, detail="PDB file not found")

#     return PlainTextResponse(content=pdb_content.decode('utf-8'))

@app.get("/data/pdb/{pdb_id}", response_class=PlainTextResponse)
async def load_pdb(pdb_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    supabase.auth.session = {"access_token": token}

    # Fetch the PDB file from Supabase storage
    try:
        pdb_content = supabase.storage.from_('pdb_files').download(f'{pdb_id}.pdb')
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"PDB file {pdb_id} not found in the database")

    return PlainTextResponse(content=pdb_content.decode('utf-8'))