#!/usr/bin/env bash

set -Eeuo pipefail

echo "Initializing CDP database..."

run_sql_directory() {
    local directory="$1"

    if [[ ! -d "$directory" ]]; then
        echo "Directory not found; skipping: $directory"
        return
    fi

    while IFS= read -r -d '' sql_file; do
        # If this SQL file creates the decision_registry table, skip it
        # when the table already exists (avoids duplicate/old DDL conflicts).
        if grep -Ei "create\s+table\s+.*decision_registry" "$sql_file" > /dev/null 2>&1; then
            if psql --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -tAc "SELECT 1 FROM pg_tables WHERE schemaname='cdp_core' AND tablename='decision_registry'" | grep -q 1; then
                echo "Skipping ${sql_file} (decision_registry already exists)"
                continue
            fi
        fi

        echo "Executing ${sql_file}"
        psql \
            --username "$POSTGRES_USER" \
            --dbname "$POSTGRES_DB" \
            --set ON_ERROR_STOP=1 \
            --file "$sql_file"
    done < <(find "$directory" -maxdepth 1 -type f -name '*.sql' -print0 | sort -z)
}

# Load any .sql files provided in the Docker-entrypoint init directory first
# (this includes 01-init-cdp.sql and any other SQL files placed beside this script)
run_sql_directory "/docker-entrypoint-initdb.d"

# Then load SQL files from the repository `db` area (mounted read-only at /cdp-init/db)
run_sql_directory "/cdp-init/db/ddl"
run_sql_directory "/cdp-init/db/seed"

echo "CDP database initialization complete."
