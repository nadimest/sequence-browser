from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from supabase import create_client, Client
import os
import glob

app = FastAPI()

# Supabase client setup
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Static files setup
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    with open("templates/index.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/data/pdb_examples", response_class=PlainTextResponse)
async def load_pdb():
    # Fetch the first PDB file from the local directory
    pdb_files = glob.glob("/data/pdb_examples/*.pdb")
    if pdb_files:
        pdb_file = pdb_files[0]
        with open(pdb_file, 'r') as file:
            pdb_content = file.read()
    else:
        pdb_content = ""
    return pdb_content
