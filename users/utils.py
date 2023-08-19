import secrets


def get_random_str(bytes_count):
    return secrets.token_hex(bytes_count)
