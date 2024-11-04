from redis.exceptions import ResponseError
from fastapi import Request
from typing import Callable
import json
from .redisConn import redis_client
from functools import wraps

# Configuración de la caché con una expiración opcional
CACHE_EXPIRATION = 60 * 5  # 5 minutos

def cache_response(expiration: int = CACHE_EXPIRATION):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Genera una clave basada en el nombre de la función y los argumentos
            key = f"{func.__name__}:{json.dumps(kwargs, sort_keys=True)}"
            
            # Verifica si ya hay un resultado en cache
            cached_response = redis_client.get(key)
            if cached_response:
                return json.loads(cached_response)
            
            # Llama a la función original
            response = await func(*args, **kwargs)
            
            # Guarda el resultado en Redis
            redis_client.setex(key, expiration, json.dumps(response))
            return response

        return wrapper
    return decorator
