import time


def delay(delay_seconds=0):
    def wrapper(func):
        def inner(*args, **kwargs):
            response = func(*args, **kwargs)
            time.sleep(delay_seconds)
            return response

        return inner

    return wrapper
