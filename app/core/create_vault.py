# Create a new vault

import uuid
import logging
import psycopg.rows
from app.db.db import conn
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)


def create_password(passphrase: str) -> str:
    """Create a new password. it must use the passphrase as salt."""
    #TODO: Implement password creation logic
    return "secure_generated_password" # Placeholder return value



def create_vault(user_id: uuid.UUID, passphrase: str) -> JSONResponse:
    """Create a new vault in the database."""
    try:
        with conn, conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            sql = """
                INSERT INTO
                    vault (user_id, passphrase)
                VALUES (%(user_id)s, %(passphrase)s)
                RETURNING id;
            """
            cursor.execute(sql, {"user_id": user_id, "passphrase": passphrase})
            vault_id = cursor.fetchone()
            logging.info(f"Vault {vault_id} created successfully")
            if not vault_id:
                raise ValueError("Failed to create new vault")

            # TODO: Implement password creation logic to return a secure password
            password = create_password(passphrase)
            """
            NOTE: It might be better to store eveything using only one transaction
            so we can consume less resources.
            """

    except Exception as e:
        logging.error(f"Database error: {e}")
        return JSONResponse(
            status_code=500, content={"message": "Internal server error"}
        )
