import os
import psycopg2
from pathlib import Path
from src.config import DB_CONFIG, DATA_DIR  # Import configuration

def parse_protein_file(file_path):
    """Parse a protein text file into a dictionary of sections."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    sections = content.split('\n## ')
    
    # Get gene name from first line (removing '# ' prefix)
    gene_name = sections[0].strip().replace('# ', '')
    
    # Create a dictionary for all sections
    data = {'gene_name': gene_name}
    
    # Parse remaining sections
    for section in sections[1:]:
        if section.strip():
            section_lines = section.strip().split('\n', 1)
            section_name = section_lines[0].lower()
            section_content = section_lines[1] if len(section_lines) > 1 else ''
            data[section_name] = section_content.strip()
    
    return data

def insert_protein(cursor, protein_data):
    """Insert protein data into the database."""
    sql = """
    INSERT INTO proteins (
        gene_name,
        overview,
        structure_description,
        function_description,
        clinical_significance,
        interactions,
        reference_list
    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    RETURNING id;
    """
    
    cursor.execute(sql, (
        protein_data['gene_name'],
        protein_data.get('overview', ''),
        protein_data.get('structure', ''),
        protein_data.get('function', ''),
        protein_data.get('clinical significance', ''),
        protein_data.get('interactions', ''),
        protein_data.get('references', '')
    ))
    return cursor.fetchone()[0]

def main():
    # Database connection parameters from config
    db_params = DB_CONFIG

    # Directory containing protein txt files from config
    data_dir = Path(DATA_DIR)
    
    print(f"Looking for .txt files in: {data_dir.absolute()}")  # Debug line
    
    # Connect to database
    conn = None
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()
        
        # Process each txt file
        files_processed = 0
        for file_path in data_dir.glob('*.txt'):
            try:
                print(f"Processing {file_path.name}...")
                protein_data = parse_protein_file(file_path)
                protein_id = insert_protein(cur, protein_data)
                print(f"Successfully inserted {file_path.name} with ID {protein_id}")
                conn.commit()
                files_processed += 1
            except Exception as e:
                print(f"Error processing {file_path.name}: {str(e)}")
                conn.rollback()
                continue
        
        print(f"\nTotal files processed: {files_processed}")
                
    except Exception as e:
        print(f"Database error: {str(e)}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()