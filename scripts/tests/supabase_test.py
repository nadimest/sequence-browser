from supabase import create_client
import logging
import os 

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Supabase setup
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

def test_supabase_connection():
    try:
        logging.info("Creating Supabase client...")
        supabase = create_client(supabase_url, supabase_key)
        
        # Get count of all records
        logging.info("Getting total count...")
        count_response = supabase.table("proteins").select("*", count='exact').execute()
        total_count = count_response.count
        logging.info(f"Total count in database: {total_count}")
        
        # Try pagination
        page_size = 1000
        all_records = []
        
        for offset in range(0, total_count, page_size):
            logging.info(f"Fetching records {offset} to {offset + page_size}...")
            response = supabase.table("proteins").select("*").range(offset, offset + page_size - 1).execute()
            all_records.extend(response.data)
            logging.info(f"Current total fetched: {len(all_records)}")
        
        logging.info(f"Final total records fetched: {len(all_records)}")
        
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        logging.error(f"Error type: {type(e)}")
        raise e

if __name__ == "__main__":
    test_supabase_connection()