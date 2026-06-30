from dataclasses import dataclass, field

from etg_scheduler.models.enums import TaskType


@dataclass
class Task:
    id: str
    name: str
    task_type: TaskType
    duration: float
    dependencies: list[str] = field(default_factory=list)
    required_specializations: list[str] = field(default_factory=list)
    required_resource_count: int = 1
    base_cost: float = 0
    description: str | None = None
