from dataclasses import dataclass, field
from datetime import datetime

from etg_scheduler.models.enums import OptimizationMode, TaskType


@dataclass
class ScheduledTask:
    task_id: str
    task_name: str
    task_type: TaskType
    start_time: float
    finish_time: float
    duration: float
    assigned_resource_ids: list[str]
    assigned_resource_names: list[str]
    cost: float


@dataclass
class ResourceUsage:
    resource_id: str
    resource_name: str
    busy_time: float
    idle_time: float
    utilization: float
    tasks_count: int


@dataclass
class ScheduleSummary:
    scenario_name: str
    optimization_mode: OptimizationMode
    total_execution_time: float
    total_cost: float
    average_resource_utilization: float
    resource_usage: list[ResourceUsage]


@dataclass
class ScheduleResult:
    scenario_name: str
    scenario_description: str
    optimization_mode: OptimizationMode
    scheduled_tasks: list[ScheduledTask]
    summary: ScheduleSummary
    algorithm: str = "Greedy"
    time_constraint: float | None = None
    created_at: datetime = field(default_factory=datetime.now)
