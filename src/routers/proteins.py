from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse, PlainTextResponse
from supabase import create_client, Client
import os

router = APIRouter()

supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

security = HTTPBearer()


@router.get("/proteins/{gene_name}")
async def search_protein_by_gene(
    gene_name: str, 
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    supabase.auth.session = {"access_token": token}

    try:
        result = supabase.table('proteins') \
            .select("*") \
            .ilike('gene_name', gene_name) \
            .execute()

        if not result.data:
            raise HTTPException(
                status_code=404, 
                detail=f"No protein found with gene name {gene_name}"
            )

        # Clean the data by replacing null values with empty strings
        cleaned_data = result.data[0]
        for key in cleaned_data:
            if cleaned_data[key] is None:
                cleaned_data[key] = ""

        return JSONResponse(content=cleaned_data)

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error searching for protein: {str(e)}"
        )


@router.get("/protein_structures/{protein_id}", response_class=PlainTextResponse)
async def load_pdb(protein_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    supabase.auth.session = {"access_token": token}

    # Fetch the PDB file from Supabase storage
    try:
        pdb_content = supabase.storage.from_('pdb_files').download(f'{protein_id}.pdb')
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"PDB file {protein_id} not found in the database")

    return PlainTextResponse(content=pdb_content.decode('utf-8'))

@router.get("/gene_suggestions/{term}")
async def get_gene_suggestions(
    term: str,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    supabase.auth.session = {"access_token": token}

    try:
        # Query Supabase for gene names that match the search term
        result = supabase.table('proteins') \
            .select('gene_name') \
            .ilike('gene_name', f'%{term}%') \
            .limit(10) \
            .execute()

        # Extract unique gene names from the results
        suggestions = list(set(item['gene_name'] for item in result.data if item['gene_name']))
        
        return JSONResponse(content=suggestions)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching gene suggestions: {str(e)}"
        )