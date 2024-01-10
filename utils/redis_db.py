import redis
import os
from dotenv import load_dotenv
load_dotenv()

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = os.getenv("REDIS_PORT", 6379)
redis_password = os.getenv("REDIS_PASSWORD", None)
redis_db = os.getenv("REDIS_DB", 0)

# decode to string automatically
redis_decode_responses = os.getenv("REDIS_DECODE_RESPONSES", True)
redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=redis_decode_responses)

def get_redis_client():
    return redis_client