from functools import wraps
from .logging_handler import log_error

def exception_handler_for_class(cls):
    for attr_name in dir(cls):
        attr = getattr(cls, attr_name)
        if callable(attr) and not attr_name.startswith("__"):  # Avoid dunder methods
            setattr(cls, attr_name, exception_handler(attr))
    return cls

def exception_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileExistsError as e:
            log_error(f"FileExistsError in {func.__name__}: {e}")
            raise
        except FileNotFoundError as e:
            log_error(f"FileNotFoundError in {func.__name__}: {e}")
            raise
        except Exception as e:
            log_error(f"Unhandled exception in {func.__name__}: {e}")
            raise
    return wrapper
