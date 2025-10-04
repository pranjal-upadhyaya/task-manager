import psutil
import time

class CPUStatCollectror:

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

        cpu_usage = cpu_usage
        return cpu_usage

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
                True