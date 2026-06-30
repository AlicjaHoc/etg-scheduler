from dataclasses import dataclass

from etg_scheduler.models.enums import ResourceType


@dataclass
class Resource:
    id: str
    name: str
    resource_type: ResourceType
    cost_per_time_unit: float
    speed_multiplier: float
    specialization: str | None = None
