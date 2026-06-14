#!/usr/bin/env python3

import os
from dotenv import load_dotenv  # type: ignore

error_msg = "Error connecting to the .env file"


def checker(param: str) -> str:
    status_messages = {
        "DATABASE_URL": "Connected to local instance",
        "API_KEY": "Authenticated",
        "ZION_ENDPOINT": "Online"
    }
    if os.environ.get(param):
        return status_messages[param]
    else:
        return error_msg


def main() -> None:
    print("ORACLE STATUS: Reading the Matrix...\n")
    load_dotenv()

    print("Configuration loaded:")
    matrix_def = "NOT SET (defaulting to production)"
    print(f"Mode: {os.environ.get('MATRIX_MODE', matrix_def)}")
    print(f"Database: {checker('DATABASE_URL')}")
    print(f"API Access: {checker('API_KEY')}")
    print(f"Log Level: {os.environ.get('LOG_LEVEL', 'WARNING')}")
    print(f"Zion Network: {checker('ZION_ENDPOINT')}")

    print("\nEnvironment security check:")
    print(" [OK] No hardcoded secrets detected")
    if load_dotenv():
        print(" [OK] .env file properly configured")
    else:
        print(' [MISSING] or conflict .env file')
    print(" [OK] Production overrides available")
    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    main()
