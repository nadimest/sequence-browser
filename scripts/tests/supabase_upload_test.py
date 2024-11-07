from supabase import create_client
import requests
import logging
import os
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Supabase setup
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

print(supabase_url, supabase_key)

def test_storage_upload():
    try:
        # Initialize Supabase client
        logging.info("Creating Supabase client...")
        supabase = create_client(supabase_url, supabase_key)
        
        # Create a session (similar to your API endpoint)
        supabase.auth.session = {"access_token": supabase_key}
        
        # Test with a single gene/protein
        gene_name = "CD5"
        uniprot_id = "P06127"
        structure_id = f"AF-{uniprot_id}-F1"
        
        # Download AlphaFold structure
        logging.info(f"Downloading AlphaFold structure for {gene_name}")
        af_url = f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_v4.pdb"
        response = requests.get(af_url)
        
        if response.status_code == 200:
            pdb_content = response.content
            
            # Try to list existing files in pdb_files bucket
            logging.info("Listing files in pdb_files bucket...")
            try:
                files = supabase.storage.from_('pdb_files').list()
                logging.info(f"Existing files: {files}")
            except Exception as e:
                logging.error(f"Error listing files: {str(e)}")
            
            # Try to upload
            logging.info(f"Attempting to upload {structure_id}.pdb")
            try:
                result = supabase.storage.from_("pdb_files").upload(
                    path=f"{structure_id}.pdb",
                    file=pdb_content,
                    file_options={
                        "content-type": "text/plain",
                        "x-upsert": "true"  # This will overwrite if file exists
                    }
                )
                logging.info(f"Upload result: {result}")
            except Exception as e:
                logging.error(f"Error during upload: {str(e)}")
                
        else:
            logging.error(f"Failed to download structure: {response.status_code}")
            
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        logging.error(f"Error type: {type(e)}")

if __name__ == "__main__":
    test_storage_upload()