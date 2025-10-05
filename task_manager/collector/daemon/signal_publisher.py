import time
from task_manager.database.redis_connector import RedisConnector
from task_manager.collector.utils.constants import RedisChannels


class SignalPublisher:
    
    def __init__(self):
        redis_connector = RedisConnector()
        self.redis_client = redis_connector.get_redis_client()

        try:
            self.redis_client.ping()
            print(f"Successfully connected to the redis client")
        except Exception as e:
            print(f"Failed to connect to the redis_client: {e}")
            raise

    def publish_signal(self, channel_name: str, message: str):

        self.redis_client.publish(
            channel = channel_name,
            message=message
        )

        print(f"Published message {message} to channel {channel_name}")

        return None

    def run(self, channel_name: str, message: str, interval: int):
        while True:
            self.publish_signal(
                channel_name=channel_name, 
                message = message
            )
            time.sleep(interval)


if __name__ == "__main__":
    channel_name = RedisChannels.TEST_CHANNEL.value
    message = "test_message"
    signal_publisher = SignalPublisher()
    signal_publisher.run(
        channel_name=channel_name,
        message=message,
        interval=10
    )