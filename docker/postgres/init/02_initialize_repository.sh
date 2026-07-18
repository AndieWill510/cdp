#!/usr/bin/env bash

set -Eeuo pipefail

echo "Initializing CDP repository database objects..."

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

# PostgreSQL's native docker-entrypoint owns top-level files in
# /docker-entrypoint-initdb.d. In particular, 01-init-cdp.sql runs before this
# 02 hook and establishes extensions and base schemas exactly once.
#
# This hook owns only repository-mounted domain DDL and optional seed data.
run_sql_directory "/cdp-init/db/ddl"
run_sql_directory "/cdp-init/db/seed"

echo "CDP repository database initialization complete."
