import functools
import time


def log_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] {func.__name__} called with args={args} kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} returned {result!r}")
        return result
    return wrapper


def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = (time.perf_counter() - start) * 1000
        print(f"[TIMED] {func.__name__} took {elapsed:.2f} ms")
        return result
    return wrapper
