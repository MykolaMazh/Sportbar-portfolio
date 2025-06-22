#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "Current working directory: $(pwd)"

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r ../requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate
export DATABASE_URL=postgresql://sportbar_db_postgre_owner:npg_xF3ljsVPdL4T@ep-wild-poetry-a2r3wplv-pooler.eu-central-1.aws.neon.tech/sportbar_db_postgre?sslmode=require
