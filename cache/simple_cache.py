from typing import Any, Dict
from typing import Callable

from functools import wraps
import time

import logging


class SimpleCache:
    def __init__(self, logger: logging.Logger = None) -> None:
        self.cache: Dict[str, Any] = {}
        self.ttl: Dict[str, float] = {}
        self.logger = logger or logging.getLogger(__name__)

    def set(self, key: str, value: Any, ttl: int):
        self.cache[key] = value
        self.ttl[key] = time.time() + ttl
        self.logger.info(f'Set cache for key: {key} with TTL: {ttl}')

    def get(self, key):
        if key in self.cache :
            if self.ttl[key] > time.time():
                self.logger.info(f'Cache hit for key: {key}')
                return self.cache[key]
            else:
                self.logger.info(f'Expired {key}, deleting')
                self.delete(key)
        self.logger.info(f'Cache miss for key: {key}')
        return None
    
    def delete(self, key: str):
        if key in self.cache:
            del self.cache[key]
            del self.ttl[key]
            self.logger.info(f'Deleted cache for key: {key}')
    
    def clear(self):
        self.cache.clear()
        self.ttl.clear()
        self.logger.info('Cleared all cache entries')