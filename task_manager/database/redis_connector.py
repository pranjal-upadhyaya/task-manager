import redis
import os
from dotenv import load_dotenv

load_dotenv()


class RedisConnector:

    def __init__(self):
        self.host = os.getenv("REDIS_HOSTNAME")
        self.port = os.getenv("REDIS_PORT")
        self.database = os.getenv("REDIS_DATABASE")

    def get_redis_client(self):
        redis_client = redis.Redis(
            host=self.host,
            port=self.port,
            db=self.database,
            decode_responses=True
        )
        return redis_client