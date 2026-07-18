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
        echo "Executing ${sql_file}"
        psql \
            --username "$POSTGRES_USER" \
            --dbname "$POSTGRES_DB" \
            --set ON_ERROR_STOP=1 \
            --file "$sql_file"
    done < <(find "$directory" -maxdepth 1 -type f -name '*.sql' -print0 | sort -z)
}

run_sql_directory "/cdp-init/ddl"
run_sql_directory "/cdp-init/seed"

echo "CDP database initialization complete."
