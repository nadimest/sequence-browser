from fastapi import APIRouter, HTTPException
from supabase import create_client, Client
import os

router = APIRouter()

supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

@router.get("/protein_structures/{protein_id}")
async def get_protein_structures(protein_id: int):
    response = supabase.table('protein_structures').select('*').eq('protein_id', protein_id).execute()
    if response.error:
        raise HTTPException(status_code=404, detail="Protein structures not found")
    return response.data
