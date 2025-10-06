import time
import psutil
from psycopg import Connection

from task_manager.collector.service.signal_subscriber import SignalSubscriber
from task_manager.collector.utils.constants import RedisChannels
from task_manager.database.postgres_connector import PostgresConnector


class MemoryMetricCollector(SignalSubscriber):

    def __init__(self):
        super().__init__()
        self.postgres_connector = PostgresConnector()

    def collect_memory_metrics(self):
        memory_usage = []
        try:
            memory_usage.append(tuple((time.time(), psutil.virtual_memory().percent)))
        except Exception as e:
            print(f"Failed to collect cpu metric: {e}")
            return []
        finally:
            return memory_usage

    def insert_memory_metrics(self, memory_metrics: list, connection: Connection):
        with connection.cursor() as cur:
            cur.executemany("INSERT INTO memory.memory_usage (timestamp, memory_usage) VALUES (%s, %s)", memory_metrics)
        connection.commit()

    def handle_signal(self, message: str, connection: Connection):
        print(f"Signal detected successfully with message: {message}")
        memory_metrics = self.collect_memory_metrics()
        if memory_metrics:
            self.insert_memory_metrics(memory_metrics, connection)
            print(f"Successfully inserted memory usage metric to DB")
        else:
            print(f"Empty memory metrics detected. Skipping database insertion.")

    def run(self, channel_name: str):

        self.pubsub.subscribe(channel_name)
        print(f"Subscribed to channel '{channel_name}'. Waiting for messages...")

        for message in self.pubsub.listen():
            if message["type"] == "message":
                message_data = message["data"]
                self.handle_signal(message=message_data)
            else:
                pass
