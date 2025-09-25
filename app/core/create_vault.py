# Create a new vault

import uuid
import logging
import psycopg.rows
from app.db.db import conn
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)

import secrets
import string

def create_password(passphrase: str) -> str:
    """Create a new password. it must use the passphrase as salt."""
    # Generate a random password
    random_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(12))
    # Combine with passphrase
    return f"{passphrase}:{random_password}"


def create_vault(user_id: uuid.UUID, passphrase: str) -> JSONResponse:
    """Create a new vault in the database."""
    try:
        with conn, conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:

            password = create_password(passphrase)

            sql = """
                INSERT INTO
                    vault (user_id, passphrase, password)
                VALUES (%(user_id)s, %(passphrase)s, %(password)s)
                RETURNING password;
            """
            cursor.execute(sql, {"user_id": user_id, "passphrase": passphrase, "password": password})
            vault_password = cursor.fetchone()
            logging.info("Vault created successfully")
            if not vault_password:
                raise ValueError("Failed to create new vault")

            return JSONResponse(status_code=201, content={"password": vault_password['password']})

    except Exception as e:
        logging.error(f"Database error: {e}")
        return JSONResponse(status_code=500, content={"message": "Internal server error"})
