from django.core.cache import cache

def cached_func(timeout=60):
    def decorator(func):
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{args}:{kwargs}"
            print(key)
            result = cache.get(key)
            print(result)
            if result is None:
                print('entrou')
                result = func(*args, **kwargs)
                cache.set(key, result, timeout)
            return result
        return wrapper
    return decorator
