from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from etg_scheduler.models.enums import OptimizationMode, TaskType


class ScheduledTask(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str
    task_name: str
    task_type: TaskType
    start_time: float
    finish_time: float
    duration: float
    assigned_resource_ids: list[str]
    assigned_resource_names: list[str]
    cost: float


class ResourceUsage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    resource_id: str
    resource_name: str
    busy_time: float
    idle_time: float
    utilization: float
    tasks_count: int


class ScheduleSummary(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scenario_name: str
    optimization_mode: OptimizationMode
    total_execution_time: float
    total_cost: float
    average_resource_utilization: float
    resource_usage: list[ResourceUsage]


class ScheduleResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scenario_name: str
    scenario_description: str
    optimization_mode: OptimizationMode
    created_at: datetime = Field(default_factory=datetime.now)
    scheduled_tasks: list[ScheduledTask]
    summary: ScheduleSummary
