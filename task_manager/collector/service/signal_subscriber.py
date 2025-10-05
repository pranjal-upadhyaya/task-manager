from task_manager.database.redis_connector import RedisConnector
from task_manager.collector.utils.constants import RedisChannels

class SignalSubscriber:

    def __init__(self):
        redis_connector = RedisConnector()
        self.redis_client = redis_connector.get_redis_client()
        self.pubsub = self.redis_client.pubsub()

    def handle_signal(self, message: str):
        print(f"Signal detected successfully with message: {message}")

    def run(self, channel_name: str):

        self.pubsub.subscribe(channel_name)
        print(f"Subscribed to channel '{channel_name}'. Waiting for messages...")

        for message in self.pubsub.listen():
            if message["type"] == "message":
                message_data = message["data"]
                self.handle_signal(message=message_data)
            else:
                pass

if __name__ == "__main__":
    channel_name = RedisChannels.TEST_CHANNEL.value
    signal_subscriber = SignalSubscriber()
    signal_subscriber.run(channel_name=channel_name)


