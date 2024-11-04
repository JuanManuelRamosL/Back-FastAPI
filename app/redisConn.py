import redis

redis_client = redis.Redis(
  host='causal-prawn-23206.upstash.io',
  port=6379,
  password='AVqmAAIjcDE1YTkyZGE3Y2M3ZmU0YWYwYjlhZWEzZjkzZDBmOWJiOXAxMA',
  ssl=True
)

redis_client.set('foo', 'bar')
print(redis_client.get('foo'))