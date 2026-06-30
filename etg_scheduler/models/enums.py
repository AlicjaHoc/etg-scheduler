from enum import Enum


class TaskType(str, Enum):
    DEDICATED = "DT"
    GENERAL = "GT"
    UNIVERSAL = "UT"
    COMMON_DEDICATED = "CDT"
    COMMON_GENERAL = "CGT"


class ResourceType(str, Enum):
    UNIVERSAL = "Universal"
    SPECIALIZED = "Specialized"


class OptimizationMode(str, Enum):
    MINIMIZE_TIME = "MinimizeTime"
    MINIMIZE_COST = "MinimizeCost"
    BALANCED = "Balanced"
