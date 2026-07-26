"""Repository modules for the live CDP core.

Every function here accepts an existing psycopg cursor from the caller's
service-level transaction. None of these functions open their own
connections or commit/roll back independently.
"""
