#!/bin/bash
set -e 

echo "Running DB Migration..."
cd /app/src/models/db_schemas/minirag/
alembic upgrade head
cd /app

exec "$@"