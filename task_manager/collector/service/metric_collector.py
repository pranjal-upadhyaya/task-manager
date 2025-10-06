
from psycopg_pool import ConnectionPool
from task_manager.collector.service.cpu_metric_collector import CPUMetricCollector
from task_manager.collector.service.memory_metric_collector import MemoryMetricCollector
import json

from task_manager.collector.service.signal_subscriber import SignalSubscriber
from task_manager.collector.utils.constants import RedisChannels
from task_manager.database.postgres_connector import PostgresConnector
from task_manager.models.commons import MetricType


class MetricCollector(SignalSubscriber):
    
    def __init__(self):
        super().__init__()
        self.postgres_connector = PostgresConnector()
        self.cpu_metric_collector = CPUMetricCollector()
        self.memory_metric_collector = MemoryMetricCollector()

    def open_connection_pool(self):
        connection_pool = self.postgres_connector.get_connection_pool()

        connection_pool.open()

        return connection_pool


    def run(self, channel_name: str, connection_pool: ConnectionPool):

        self.pubsub.subscribe(channel_name)
        print(f"Subscribed to channel '{channel_name}'. Waiting for messages...")

        with connection_pool.connection() as connection:

            for message in self.pubsub.listen():
                if message["type"] == "message":
                    message_data = json.loads(message["data"])
                    if message_data["metric_type"] == MetricType.CPU_USAGE_PERCENT.value:
                        self.cpu_metric_collector.handle_signal(message=message_data, connection=connection)
                    else:
                        self.memory_metric_collector.handle_signal(message=message_data, connection=connection)
                else:
                    pass

    def close_connection_pool(self, connection_pool: ConnectionPool):

        connection_pool.close()

        return None

if __name__ == "__main__":
    metrics_collector = MetricCollector()
    channel_name = RedisChannels.TEST_CHANNEL.value
    connection_pool = metrics_collector.open_connection_pool()
    try:
        while True:
            metrics_collector.run(channel_name=channel_name, connection_pool=connection_pool)
    except KeyboardInterrupt as e:
        print(f"Keyboard exception detected: {e}. Closing session")
        metrics_collector.close_connection_pool(connection_pool)
    except Exception as e:
        print(f"Unexpected error detected: {e}. Closing session")
        metrics_collector.close_connection_pool(connection_pool)
    finally:
        pass