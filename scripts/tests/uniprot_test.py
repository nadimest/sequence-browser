import requests
from datetime import datetime

def get_pdb_structures_from_rcsb(uniprot_id):
    """Try to get PDB structures from RCSB using UniProt ID"""
    url = f"https://data.rcsb.org/rest/v1/core/uniprot/{uniprot_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # The response includes PDB IDs mapped to this UniProt ID
        return data.get('rcsb_id_list', [])
    return []

def get_alphafold_structure(uniprot_id):
    """Check if AlphaFold structure exists"""
    # AlphaFold database URL pattern
    url = f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_v4.pdb"
    response = requests.head(url)  # Use HEAD request to check existence
    return url if response.status_code == 200 else None

def get_pdb_metadata(pdb_id):
    """Get metadata for a PDB structure including deposition date"""
    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            'id': pdb_id,
            'deposition_date': data.get('rcsb_accession_info', {}).get('deposit_date', ''),
            'method': data.get('exptl', [{}])[0].get('method', '')
        }
    return None

# Test with one gene first
test_data = [
    ("TP53", "P04637"),
    ("DIRAS2", "Q96HU8"),
    ("GBP2", "P32456"),
    ("CILK1", "Q9UPZ9"),
    ("MRPS11", "P82912")
]

for gene_name, uniprot_id in test_data:
    print(f"\nProcessing {gene_name} (UniProt: {uniprot_id})")
    
    # Try RCSB PDB first
    pdb_ids = get_pdb_structures_from_rcsb(uniprot_id)
    
    if pdb_ids:
        print(f"Found {len(pdb_ids)} PDB structures:")
        # Get metadata for each structure
        structures = []
        for pdb_id in pdb_ids:
            metadata = get_pdb_metadata(pdb_id)
            if metadata:
                structures.append(metadata)
        
        # Sort by deposition date and get the latest
        if structures:
            latest = sorted(structures, 
                          key=lambda x: datetime.strptime(x['deposition_date'], '%Y-%m-%d'), 
                          reverse=True)[0]
            print(f"Latest structure: {latest['id']}")
            print(f"Deposition date: {latest['deposition_date']}")
            print(f"Method: {latest['method']}")
    else:
        # Try AlphaFold
        alphafold_url = get_alphafold_structure(uniprot_id)
        if alphafold_url:
            print(f"Found AlphaFold structure: {alphafold_url}")
        else:
            print("No structures found in either PDB or AlphaFold")