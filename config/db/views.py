import psycopg2
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from config.utils.custom_decorator import staff_or_superuser_required

from .pg_config import get_pg_config


def format_bytes(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    for unit in ("KB", "MB", "GB", "TB"):
        size_bytes /= 1024
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
    return f"{size_bytes:.1f} PB"


def get_pg_connection():
    cfg = get_pg_config()
    return psycopg2.connect(
        host=cfg["HOST"],
        port=cfg["PORT"],
        user=cfg["USER"],
        password=cfg["PASSWORD"],
        dbname=cfg["NAME"],
    )


def get_database_details():
    conn = get_pg_connection()
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    d.datname AS name,
                    pg_catalog.pg_get_userbyid(d.datdba) AS owner,
                    pg_catalog.pg_size_pretty(pg_catalog.pg_database_size(d.datname)) AS size,
                    pg_catalog.pg_database_size(d.datname) AS size_bytes,
                    (SELECT count(*) FROM pg_stat_activity WHERE datname = d.datname) AS connections,
                    d.datcollate AS collation,
                    d.datctype AS ctype
                FROM pg_catalog.pg_database d
                WHERE d.datistemplate = false
                ORDER BY size_bytes DESC
            """)
            columns = [col[0] for col in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]
    finally:
        conn.close()


@login_required
@staff_or_superuser_required
def db_dashboard(request):
    cfg = get_pg_config()
    error = None
    database_details = []
    try:
        database_details = get_database_details()
    except Exception as e:
        error = str(e)

    total_size_bytes = sum(db["size_bytes"] for db in database_details)
    total_connections = sum(db["connections"] for db in database_details)

    context = {
        "databases": database_details,
        "error": error,
        "total_dbs": len(database_details),
        "total_size": format_bytes(total_size_bytes),
        "total_size_bytes": total_size_bytes,
        "total_connections": total_connections,
        "db_name": cfg["NAME"],
        "db_user": cfg["USER"],
        "db_host": cfg["HOST"],
        "db_port": cfg["PORT"],
    }
    return render(request, "db/postgres_dashboard.html", context)
