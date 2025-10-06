import enum

class RedisChannels(str, enum.Enum):
    TEST_CHANNEL = "TEST_CHANNEL"
    CPU_CHANNEL = "CPU_CHANNEL"
    MEMORY_CHANNEL = "MEMORY_CHANNEL"