from json.encoder import JSONEncoder
import time
from task_manager.database.redis_connector import RedisConnector
from task_manager.collector.utils.constants import RedisChannels
from task_manager.models.commons import MetricType
import json


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

    def publish_signal(self, channel_name: str, message: dict):

        message = json.dumps(message)

        self.redis_client.publish(
            channel = channel_name,
            message=message
        )

        print(f"Published message {message} to channel {channel_name}")

        return None

    def create_message(self):

        message = {}

        message["metric_type"] = MetricType.CPU_USAGE_PERCENT.value

        return message

    def run(self, channel_name: str, message: dict, interval: int):
        while True:
            self.publish_signal(
                channel_name=channel_name, 
                message = message
            )
            time.sleep(interval)


if __name__ == "__main__":
    channel_name = RedisChannels.TEST_CHANNEL.value
    signal_publisher = SignalPublisher()
    message = signal_publisher.create_message()
    try:
        signal_publisher.run(
            channel_name=channel_name,
            message=message,
            interval=10
        )
    except KeyboardInterrupt as e:
        print(f"Keyboard exception detected: {e}. Closing session")
    except Exception as e:
        print(f"Unexpected error detected: {e}. Closing session")
    finally:
        pass