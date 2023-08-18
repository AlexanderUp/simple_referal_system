import os


def generate_code(length):
    def inner():
        return os.urandom(length / 2).hex()

    return inner
