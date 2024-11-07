## Database Setup

This project includes a basic database schema for storing protein information. While currently using a simple setup script, we're structuring the project to support proper schema migrations in the future.

### Why Migrations Matter

As this application grows and potentially supports multiple installations or tenants, we'll need a robust way to:
- Track database schema versions
- Support upgrades and rollbacks
- Handle tenant-specific customizations
- Maintain data integrity during schema changes

### Current Setup

For now, we're keeping it simple with:
- A single initial schema file (`001_initial_schema.sql`)
- A basic Python setup script (`setup_db.py`)

### Future Migration Plans

We plan to implement:
- Version tracking for schema changes
- Support for upgrade and rollback scripts
- Tenant-specific schema management
- Migration history logging

## Setup Instructions

1. Set your environment variables:
```bash
export DB_NAME=your_db_name
export DB_USER=your_username
export DB_PASSWORD=your_password
export DB_HOST=localhost
export DB_PORT=5432
```

2. Run the database setup:
```bash
python migrations/setup_db.py
```

3. Populate initial data:
```bash
python src/populate_proteins.py
```

## Project Structure
```
project_root/
├── migrations/
│   ├── 001_initial_schema.sql
│   └── setup_db.py
├── src/
│   └── populate_proteins.py
└── README.md
```