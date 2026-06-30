import json
from pathlib import Path

from etg_scheduler.models.enums import OptimizationMode, ResourceType, TaskType
from etg_scheduler.models.resource import Resource
from etg_scheduler.models.scenario import Scenario
from etg_scheduler.models.task import Task


class ScenarioLoader:
    def __init__(self, scenarios_dir: Path | str = "scenarios") -> None:
        self.scenarios_dir = Path(scenarios_dir)

    def list_scenarios(self) -> list[Path]:
        if not self.scenarios_dir.exists():
            return []
        return sorted(self.scenarios_dir.glob("*.json"))

    def load(self, path: Path | str) -> Scenario:
        scenario_path = Path(path)
        if not scenario_path.exists():
            raise FileNotFoundError(f"Scenario file not found: {scenario_path}")

        with scenario_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        tasks = [self._load_task(item) for item in data.get("tasks", [])]
        resources = [self._load_resource(item) for item in data.get("resources", [])]
        return Scenario(
            name=data.get("name", ""),
            description=data.get("description", ""),
            tasks=tasks,
            resources=resources,
            default_optimization_mode=OptimizationMode(
                data.get("default_optimization_mode", OptimizationMode.BALANCED.value)
            ),
        )

    def _load_task(self, data: dict) -> Task:
        return Task(
            id=data.get("id", ""),
            name=data.get("name", ""),
            task_type=TaskType(data.get("task_type", "")),
            duration=float(data.get("duration", 0)),
            dependencies=list(data.get("dependencies", [])),
            required_specializations=list(data.get("required_specializations", [])),
            required_resource_count=int(data.get("required_resource_count", 1)),
            base_cost=float(data.get("base_cost", 0)),
            description=data.get("description"),
        )

    def _load_resource(self, data: dict) -> Resource:
        return Resource(
            id=data.get("id", ""),
            name=data.get("name", ""),
            resource_type=ResourceType(data.get("resource_type", "")),
            specialization=data.get("specialization"),
            cost_per_time_unit=float(data.get("cost_per_time_unit", 0)),
            speed_multiplier=float(data.get("speed_multiplier", 0)),
        )
