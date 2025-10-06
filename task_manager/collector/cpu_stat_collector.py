import psutil
import time
from task_manager.database.postgres_connector import PostgresConnector

class CPUStatCollector:

    def get_cpu_usage(self, collection_interval: int, collection_count: int):
        """
        Get the CPU usage for a given collection period.
        """
        cpu_usage = []
        
        for _ in range(collection_count+1):
            start_time = time.time()
            cpu_usage.append(tuple((time.time(), psutil.cpu_percent())))

            elapsed_time = time.time() - start_time
            remaining_time = collection_interval - elapsed_time
            if remaining_time > 0:
                time.sleep(remaining_time)

        return cpu_usage[1:]


    def insert_cpu_usage(self, cpu_usage: list):
        postgres_connector = PostgresConnector()
        conn = postgres_connector.connect()
        cursor = conn.cursor()
        cursor.executemany("INSERT INTO cpu.cpu_usage (timestamp, cpu_usage) VALUES (%s, %s)", cpu_usage)
        conn.commit()
        cursor.close()
        conn.close()

    def get_async_cpu_usage(self, collection_interval: int):
        """
        Get the CPU usage for a given collection period.
        """
        cpu_usage = []
        while True:
            try:
                start_time = time.time()
                cpu_usage.append(tuple((time.time(), psutil.cpu_percent())))

                elapsed_time = time.time() - start_time
                remaining_time = collection_interval - elapsed_time
                if remaining_time > 0:
                    time.sleep(remaining_time)
            except KeyboardInterrupt:
                print("KeyboardInterrupt")
                return cpu_usage
            except Exception as e:
                print(e)
                return cpu_usage
            finally:
                pass