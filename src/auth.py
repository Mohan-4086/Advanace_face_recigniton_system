"""Salted password hashing using Python's standard library."""
import hashlib
import hmac
import secrets


def hash_password(password):
    salt = secrets.token_hex(16)
    rounds = 600000
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), rounds).hex()
    return f"pbkdf2_sha256${rounds}${salt}${digest}"


def verify_password(password, stored):
    try:
        algorithm, rounds, salt, expected = stored.split("$")
        rounds = int(rounds)
        if algorithm != "pbkdf2_sha256" or not 100000 <= rounds <= 2000000:
            return False
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), rounds).hex()
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError, AttributeError):
        return False
