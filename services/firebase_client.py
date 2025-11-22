import os

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore

load_dotenv()

_db = None


def init_app():
    global _db

    if _db is not None:
        return _db

    credential_path = os.getenv("FIREBASE_CREDENTIALS_PATH")

    if not credential_path:
        raise RuntimeError(
            "FIREBASE_CREDENTIALS_PATH environment variable is not set."
        )

    cred = credentials.Certificate(credential_path)
    firebase_admin.initialize_app(cred)
    _db = firestore.client()

    return _db


def get_db():
    return _db or init_app()
