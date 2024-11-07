from fastapi import APIRouter, HTTPException
from supabase import create_client, Client
import os

router = APIRouter()

supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

@router.get("/proteins/search")
async def search_proteins(query: str):
    response = supabase.table('proteins').select('*').ilike('gene_name', f'%{query}%').execute()
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return response.data

@router.get("/proteins/{protein_id}")
async def get_protein(protein_id: int):
    response = supabase.table('proteins').select('*').eq('id', protein_id).single().execute()
    if response.error:
        raise HTTPException(status_code=404, detail="Protein not found")
    return response.data
