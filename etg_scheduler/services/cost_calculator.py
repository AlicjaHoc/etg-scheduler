from __future__ import annotations

from etg_scheduler.models.resource import Resource
from etg_scheduler.models.task import Task


class CostCalculator:
    def adjusted_duration(self, task: Task, resources: list[Resource]) -> float:
        average_speed = sum(resource.speed_multiplier for resource in resources) / len(resources)
        return task.duration / average_speed

    def task_cost(self, task: Task, resources: list[Resource], adjusted_duration: float) -> float:
        resource_cost = sum(resource.cost_per_time_unit for resource in resources) * adjusted_duration
        return resource_cost + task.base_cost
