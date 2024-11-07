import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import requests
from supabase import create_client, Client
import logging
import sys
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)

# Supabase client setup
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

def get_all_gene_names():
    """Fetch all gene names using pagination"""
    logging.info("Starting to fetch all gene names...")
    
    # Get total count
    count_response = supabase.table("proteins").select("*", count='exact').is_("structure_id", "null").execute()
    total_count = count_response.count
    logging.info(f"Total records to process: {total_count}")
    
    # Fetch all records using pagination
    page_size = 1000
    all_gene_names = []
    
    for offset in range(0, total_count, page_size):
        logging.info(f"Fetching records {offset} to {offset + page_size}...")
        response = supabase.table("proteins").select("gene_name").is_("structure_id", "null").range(offset, offset + page_size - 1).execute()
        all_gene_names.extend([record['gene_name'] for record in response.data])
        logging.info(f"Current total fetched: {len(all_gene_names)}")
    
    logging.info(f"Final total gene names fetched: {len(all_gene_names)}")
    return all_gene_names

class GetUniprotID(beam.DoFn):
    def process(self, gene_name):
        logging.info(f"Processing gene: {gene_name}")
        url = f"https://rest.uniprot.org/uniprotkb/search?query=gene:{gene_name}+AND+organism_id:9606&format=json"
        try:
            response = requests.get(url)
            logging.info(f"UniProt API response status for {gene_name}: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                if data['results']:
                    uniprot_id = data['results'][0]['primaryAccession']
                    logging.info(f"Found UniProt ID for {gene_name}: {uniprot_id}")
                    return [(gene_name, uniprot_id)]
                else:
                    logging.warning(f"No UniProt results for {gene_name}")
            else:
                logging.error(f"Error response from UniProt for {gene_name}: {response.text}")
        except Exception as e:
            logging.error(f"Exception processing {gene_name}: {str(e)}")
        return []

class GetAlphaFoldStructure(beam.DoFn):
    def process(self, element):
        gene_name, uniprot_id = element
        logging.info(f"Fetching AlphaFold structure for {gene_name} ({uniprot_id})")
        url = f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_v4.pdb"
        try:
            response = requests.get(url)
            logging.info(f"AlphaFold API response status for {gene_name}: {response.status_code}")
            if response.status_code == 200:
                structure_id = f"AF-{uniprot_id}-F1"
                logging.info(f"Successfully downloaded structure for {gene_name}: {structure_id}")
                return [(gene_name, structure_id, response.content)]
            else:
                logging.warning(f"No AlphaFold structure found for {gene_name}")
        except Exception as e:
            logging.error(f"Exception downloading structure for {gene_name}: {str(e)}")
        return []

class SaveToSupabase(beam.DoFn):
    def process(self, element):
        gene_name, structure_id, pdb_content = element
        logging.info(f"Saving {gene_name} structure to Supabase")
        
        file_name = f"{structure_id}.pdb"
        try:
            # Save to Supabase bucket
            logging.info(f"Uploading {file_name} to Supabase bucket")
            supabase.storage.from_("pdb_files").upload(
                path=file_name,
                file=pdb_content,
                file_options={"content-type": "text/plain"}
            )
            
            # Update database
            logging.info(f"Updating database record for {gene_name}")
            supabase.table("proteins").update(
                {"structure_id": structure_id}
            ).eq("gene_name", gene_name).execute()
            
            logging.info(f"Successfully processed {gene_name}")
            return [(gene_name, structure_id, "success")]
        except Exception as e:
            logging.error(f"Error processing {gene_name}: {str(e)}")
            return [(gene_name, None, f"error: {str(e)}")]

def run_pipeline():
    # Pipeline options
    options = PipelineOptions()

    logging.info("Starting pipeline")
    
    try:
        # Get all gene names with pagination
        gene_names = get_all_gene_names()
        logging.info(f"Retrieved {len(gene_names)} genes to process")
        
        with beam.Pipeline(options=options) as p:
            # Create initial PCollection from gene names
            genes = p | "Create gene names" >> beam.Create(gene_names)

            # Get UniProt IDs
            uniprot_ids = genes | "Get UniProt IDs" >> beam.ParDo(GetUniprotID())

            # Get AlphaFold structures
            structures = uniprot_ids | "Get AlphaFold structures" >> beam.ParDo(GetAlphaFoldStructure())

            # Save to Supabase
            results = structures | "Save to Supabase" >> beam.ParDo(SaveToSupabase())

            # Log results
            results | "Log Results" >> beam.Map(lambda x: logging.info(f"Pipeline result: {x}"))

    except Exception as e:
        logging.error(f"Pipeline error: {str(e)}")
        raise e

if __name__ == "__main__":
    logging.info("Script started")
    run_pipeline()
    logging.info("Script finished")