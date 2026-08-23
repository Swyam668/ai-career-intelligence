# import redis.asyncio as redis


# REDIS_URL = "redis://localhost:6379/0"


# redis_client = redis.from_url(
#     REDIS_URL,
#     encoding="utf-8",
#     # redis stores/returns bytes by default. with this enabled:
#     # await redis_client.get("key") 
#     # returns a normal Python str, so JSON caching easier.
#     decode_responses=True
# )

from upstash_redis.asyncio import Redis


redis_client = Redis.from_env()