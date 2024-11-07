CREATE TABLE IF NOT EXISTS proteins (
    id SERIAL PRIMARY KEY,
    gene_name VARCHAR(255) NOT NULL,
    overview TEXT,
    structure_description TEXT,
    function_description TEXT,
    clinical_significance TEXT,
    interactions TEXT,
    reference_list TEXT,
    pdb_structure TEXT,
    pdb_date DATE,
    structure_source VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);