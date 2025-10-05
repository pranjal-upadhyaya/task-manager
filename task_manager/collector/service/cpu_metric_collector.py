import psutil
import time
from task_manager.collector.utils.constants import RedisChannels
from task_manager.database.postgres_connector import PostgresConnector
from task_manager.collector.service.signal_subscriber import SignalSubscriber


class CPUMetricCollector(SignalSubscriber):

    def __init__(self):
        super().__init__()
        self.postgres_connector = PostgresConnector()
        self.conn = None
        self.cursor = None

    def open_db_connection(self):
        self.conn = self.postgres_connector.connect()
        self.cursor = self.conn.cursor()

    def close_db_connection(self):
        self.cursor.close()
        self.conn.close()

    def collect_cpu_metrics(self):
        cpu_usage = []
        try:
            cpu_usage.append(tuple((time.time(), psutil.cpu_percent())))
        except Exception as e:
            print(f"Failed to collect cpu metric: {e}")
            return []
        finally:
            return cpu_usage

    def insert_cpu_metrics(self, cpu_metrics: list):
        self.cursor.executemany("INSERT INTO cpu.cpu_usage (timestamp, cpu_usage) VALUES (%s, %s)", cpu_metrics)
        self.conn.commit()

    def handle_signal(self, message: str):
        print(f"Signal detected successfully with message: {message}")
        cpu_metrics = self.collect_cpu_metrics()
        if cpu_metrics:
            self.insert_cpu_metrics(cpu_metrics)
            print(f"Successfully inserted cpu usage metric to DB")
        else:
            print(f"Empty cpu metrics detected. Skipping database insertion.")

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
    cpu_metric_collector = CPUMetricCollector()
    cpu_metric_collector.open_db_connection()
    try:
        while True:
            cpu_metric_collector.run(channel_name=channel_name)
    except KeyboardInterrupt as e:
        print(f"Keyboard exception detected: {e}. Closing session")
        cpu_metric_collector.close_db_connection()
    except Exception as e:
        print(f"Unexpected error detected: {e}. Closing session")
        cpu_metric_collector.close_db_connection()
    finally:
        pass


    