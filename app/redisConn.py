import redis

try:
    redis_client = redis.Redis(
        host="star-marmoset-17924.upstash.io",
        port=6379,
        password="AUYEAAIjcDFlN2M5YTIwZjMwN2Y0ODU5OTg4ZDlkM2NmYzhkM2ZjZnAxMA",
        ssl=True,
        decode_responses=True  # Para que los valores sean strings en vez de bytes
    )

    redis_client.set("foo", "bar")
    value = redis_client.get("foo")
    print(f"✅ Conectado a Redis. Valor almacenado: {value}")
except Exception as e:
    print(f"❌ Error de conexión a Redis: {e}")
