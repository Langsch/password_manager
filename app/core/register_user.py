# User registration and validation logic

import logging
import psycopg.rows
import bcrypt
from app.db.db import conn
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)


def validate_password(password: str) -> bool:
    """Efficient password validation with single pass."""
    if len(password) < 8:
        return False

    has_lower = has_upper = has_digit = has_special = False
    digit_count = special_count = 0

    for char in password:
        if char.islower():
            has_lower = True
        elif char.isupper():
            has_upper = True
        elif char.isdigit():
            has_digit = True
            digit_count += 1
        elif not char.isalnum():
            has_special = True
            special_count += 1

    return (
        has_lower
        and has_upper
        and has_digit
        and has_special
        and digit_count >= 4
        and special_count >= 2
    )


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""

    # converting password to array of bytes
    bytes_array = password.encode("utf-8")

    # generating the salt
    salt = bcrypt.gensalt()

    # Hashing the password
    password_hash = bcrypt.hashpw(bytes_array, salt)

    return password_hash.decode("utf-8")


def register_user(email: str, password: str, confirmation: str) -> JSONResponse:
    """Register a new user with validation and database insertion."""

    if password != confirmation:
        return JSONResponse(
            status_code=400,
            content={"message": "Password and confirmation do not match."},
        )

    if not validate_password(password):
        return JSONResponse(
            status_code=400,
            content={"message": "Password does not meet complexity requirements."},
        )

    try:
        with conn, conn.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            # Check if user already exists
            sql = """
                SELECT exists(
                    SELECT 1
                    FROM "user" u
                    WHERE u."email" = %(email)s
                )
            """

            cursor.execute(sql, {"email": email})
            if cursor.fetchone() == {"exists": True}:
                return JSONResponse(
                    status_code=409, content={"message": "User already exists."}
                )

            password = hash_password(password)

            sql = """
                INSERT INTO "user"
                    (email, password)
                VALUES
                    (%(email)s, %(password)s)
                RETURNING email
            """
            # Insert new user
            cursor.execute(sql, {"email": email, "password": password})

            new_user = cursor.fetchone()
            if not new_user:
                raise ValueError("User registration failed.")

            logging.info(f"Registering user: {new_user}")

            return JSONResponse(
                status_code=201, content={"message": "User registered successfully."}
            )

    except Exception as e:
        return JSONResponse(
            status_code=500, content={"message": f"Registration failed: {str(e)}"}
        )
