import secrets


def generate_secret_key(length=32):
    """Generate a secure random secret key."""
    return secrets.token_hex(length)


# Generate and print secret keys
print("Flask Secret Key:", generate_secret_key())
print("JWT Secret Key:", generate_secret_key())
