# Login business logic

import bcrypt
import logging
import psycopg.rows
from fastapi.responses import JSONResponse, Response
from app.db.db import conn
from app.domain.auth import User

logging.basicConfig(level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)


def unhash_password(stored_password: str, provided_password: str) -> bool:
    """Check a provided password against the stored hashed password."""
    check = bcrypt.checkpw(
        provided_password.encode("utf-8"), stored_password.encode("utf-8")
    )
    logging.info(f"Password verification result: {check}")
    return check


def authenticate(email: str, password: str) -> JSONResponse | Response:
    try:
        with conn, conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            sql = """
                SELECT u."password"
                FROM "user" u
                WHERE u."email" = %(email)s
            """
            cursor.execute(sql, {"email": email})
            user = cursor.fetchone()
            if not user:
                logging.info(
                    f"Authentication failed: User with email {email} not found."
                )
                return JSONResponse(
                    status_code=401, content={"message": "Invalid email or password."}
                )

            if unhash_password(user["password"], password):
                logging.info(f"User with email {email} authenticated successfully.")
                return Response(status_code=200)

            logging.info(
                f"Authentication failed: Invalid password for user with email {email}."
            )
            return JSONResponse(
                status_code=401, content={"message": "Invalid email or password."}
            )

    except Exception as e:
        logging.error(f"Database error: {e}")
        return JSONResponse(
            status_code=500, content={"message": "Internal server error"}
        )
