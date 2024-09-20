from fastapi import FastAPI
import uvicorn

import logging

from cache import SimpleCache, CacheManager



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()
cache = SimpleCache(logger=logger)
cache_manager = CacheManager(cache=cache)


@app.get('/{item_id}')
@cache_manager.cache_response(key='item_{item_id}', ttl=10)
async def get_item(item_id: int):
    return {'item_id': item_id}



if __name__ == '__main__': 
    uvicorn.run('test:app', reload=True)