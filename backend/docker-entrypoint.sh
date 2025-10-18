#!/bin/bash
set -e

echo "=========================================="
echo "Starting Moderation Engine Backend"
echo "=========================================="

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h postgres -p 5432 -U postgres; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done

echo "PostgreSQL is ready!"
echo ""

# Initialize database with seed data
echo "Initializing database..."
python init_db.py
echo "Database initialization complete!"
echo ""

# Start the application
echo "Starting FastAPI application..."
echo "=========================================="
exec "$@"
