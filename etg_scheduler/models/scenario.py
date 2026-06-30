from dataclasses import dataclass

from etg_scheduler.models.enums import OptimizationMode
from etg_scheduler.models.resource import Resource
from etg_scheduler.models.task import Task


@dataclass
class Scenario:
    name: str
    description: str
    tasks: list[Task]
    resources: list[Resource]
    default_optimization_mode: OptimizationMode = OptimizationMode.BALANCED
