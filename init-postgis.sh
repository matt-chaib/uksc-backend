#!/bin/bash
# This script will be run by PostgreSQL upon initialization

# Ensure the PostGIS extension is created
echo "Creating PostGIS extension..."
psql -U postgres -d food_supplier_db -c "CREATE EXTENSION IF NOT EXISTS postgis;"
