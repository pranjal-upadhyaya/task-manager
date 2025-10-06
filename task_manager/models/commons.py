import enum

class MetricType(str, enum.Enum):
    CPU_USAGE_PERCENT = "CPU_USAGE_PERCENT"
    MEMORY_USAGE_PERCENT = "MEMORY_USAGE_PERCENT"