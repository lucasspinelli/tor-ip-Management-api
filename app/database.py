import psycopg2
from psycopg2.extras import RealDictCursor
import os

# Configuração do PostgreSQL usando variáveis de ambiente
POSTGRES_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "excluded_ips_db"),
    "user": os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", "1234"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": int(os.getenv("POSTGRES_PORT", 5432)),
}

def get_db():
    try:
        conn = psycopg2.connect(
            dbname=POSTGRES_CONFIG["dbname"],
            user=POSTGRES_CONFIG["user"],
            password=POSTGRES_CONFIG["password"],
            host=POSTGRES_CONFIG["host"],
            port=POSTGRES_CONFIG["port"]
        )
        return conn
    except Exception as e:
        raise ConnectionError(f"Failed to connect database: {e}")

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS excluded_ips (
                id SERIAL PRIMARY KEY,
                ip TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise ValueError(f"Failed on init database: {e}")
    finally:
        conn.close()

def insert_excluded_ip(ip):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO excluded_ips (ip) VALUES (%s)", (ip,))
        conn.commit()
    except psycopg2.IntegrityError:
        conn.rollback()
        raise ValueError(f"The IP {ip} is already on exclusion list.")
    except Exception as e:
        conn.rollback()
        raise ValueError(f"Error on insert the IP: {e}")
    finally:
        conn.close()

def get_excluded_ips():
    conn = get_db()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT ip FROM excluded_ips")
        ips = {row["ip"] for row in cursor.fetchall()}
        return ips
    except Exception as e:
        raise ValueError(f"Error on get excluded IPs: {e}")
    finally:
        conn.close()

def delete_excluded_ip(ip):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM excluded_ips WHERE ip = %s", (ip,))
        changes = cursor.rowcount
        conn.commit()
        if changes == 0:
            raise ValueError(f"The {ip} is not on the exclusion list.")
    except Exception as e:
        conn.rollback()
        raise ValueError(f"Error trying to remove the IP: {e}")
    finally:
        conn.close()



