import requests
import json

def search_pdb_by_gene(gene_name):
    url = "https://search.rcsb.org/rcsbsearch/v2/query"
    
    query = {
        "query": {
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": "rcsb_gene_name.value",
                "operator": "contains_words",
                "value": gene_name
            }
        },
        "return_type": "entry"
    }
    
    response = requests.post(url, json=query)
    results = json.loads(response.text)
    
    return [result["identifier"] for result in results.get("result_set", [])]

def download_pdb_file(pdb_id):
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(f"{pdb_id}.pdb", "wb") as file:
            file.write(response.content)
        print(f"PDB file {pdb_id}.pdb downloaded successfully.")
        return True
    else:
        print(f"Failed to download PDB file for {pdb_id}.")
        return False

def process_gene(gene_name):
    print(f"Processing gene: {gene_name}")
    pdb_ids = search_pdb_by_gene(gene_name)
    
    if pdb_ids:
        print(f"Found PDB IDs for {gene_name}: {', '.join(pdb_ids)}")
        for pdb_id in pdb_ids:
            download_pdb_file(pdb_id)
    else:
        print(f"No PDB structures found for gene {gene_name}")

# Example usage
gene_name = "TP53"  # Replace with your gene name
process_gene(gene_name)