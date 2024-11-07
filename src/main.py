from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import os
from src.routers import proteins, auth  # Import the routers

app = FastAPI()

# Supabase client setup
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Static files setup
app.mount("/static", StaticFiles(directory="static"), name="static")

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    with open("templates/index.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/main_app", response_class=HTMLResponse)
async def main_app():
    with open("templates/main_app.html") as f:
        return HTMLResponse(content=f.read())

# Include the routers
app.include_router(proteins.router, prefix="/api")
app.include_router(auth.router, prefix="/auth")