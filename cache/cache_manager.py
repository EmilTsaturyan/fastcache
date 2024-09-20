from typing import Callable
from functools import wraps

from .simple_cache import SimpleCache


class CacheManager:
    def __init__(self, cache):
        self.cache: SimpleCache = cache

    def cache_response(self, key: str, ttl: int):
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                cached = self.cache.get(key)
                if cached:
                    return cached
                result = await func(*args, **kwargs)
                self.cache.set(key, result, ttl)
                return result
            return wrapper
        return decorator


simple_cache = SimpleCache()
cache_manager = CacheManager(cache=simple_cache)