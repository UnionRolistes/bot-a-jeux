

log_requested = False

def logger(func):
    def wrapper(*args, **kwargs):
        ok = func(*args, **kwargs)
        if log_requested:
            print("{}{}".format(func.__name__, args[1:]))
        return ok
    return wrapper