# Sequence Browser

## [Live Demo](#)

## Description
This is an application to browse genes and proteins. It provides a user-friendly browser including 3D visualization of the structure and some curated reference information.

## Architecture
- **Backend**: FastAPI app
- **Frontend**: HTMX with minimal JavaScript modules for enhanced functionality
- **Database**: Supabase instance including Postgres
- **Authentication**: Supabase user management and authentication
- **Storage**: Supabase object storage for storing PDB files

## Data Pipeline Scripts
- **Populate Proteins**: ETL pipeline to populate the Postgres instance with protein data.
- **Populate Structures**: ETL pipeline to populate the Postgres instance with protein structure data.

## Deployment
- **Docker**: Dockerfile and docker-compose for local testing
- **Cloud Deployment**: Ready to be deployed as a cloud app (Digital Ocean, Google Cloud Run, etc.)

## Setup Instructions
1. **Set Environment Variables**:
    ```bash
    export DB_NAME=your_db_name
    export DB_USER=your_username
    export DB_PASSWORD=your_password
    export DB_HOST=localhost
    export DB_PORT=5432
    export SUPABASE_URL=your_supabase_url
    export SUPABASE_KEY=your_supabase_key
    ```

2. **Run Database Setup**:
    ```bash
    python migrations/setup_db.py
    ```

3. **Populate Initial Data**:
    ```bash
    python src/populate_proteins.py
    python src/populate_structures.py
    ```

## Running the Application
1. **Build and Run with Docker**:
    ```bash
    docker-compose up --build
    ```

2. **Access the Application**:
    Open your browser and navigate to `http://localhost:8000`

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.