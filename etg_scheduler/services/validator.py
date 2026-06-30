from __future__ import annotations

import networkx as nx

from etg_scheduler.models.enums import TaskType
from etg_scheduler.models.scenario import Scenario
from etg_scheduler.models.validation import ValidationResult
from etg_scheduler.services.resource_matcher import ResourceMatcher


class ScenarioValidator:
    def __init__(self, matcher: ResourceMatcher | None = None) -> None:
        self.matcher = matcher or ResourceMatcher()

    def validate(self, scenario: Scenario) -> ValidationResult:
        errors: list[str] = []
        warnings: list[str] = []
        tasks_by_id = {task.id: task for task in scenario.tasks}
        resources_by_id = {resource.id: resource for resource in scenario.resources}

        if len(tasks_by_id) != len(scenario.tasks):
            errors.append("Task IDs must be unique.")
        if len(resources_by_id) != len(scenario.resources):
            errors.append("Resource IDs must be unique.")

        self._validate_task_rules(scenario, errors)
        self._validate_dependencies(scenario, tasks_by_id, errors)
        self._validate_graph(scenario, errors)
        self._validate_assignments(scenario, errors)
        self._validate_unused_resources(scenario, warnings)

        return ValidationResult(errors=errors, warnings=warnings)

    def _validate_task_rules(self, scenario: Scenario, errors: list[str]) -> None:
        for task in scenario.tasks:
            if task.id in task.dependencies:
                errors.append(f"Task {task.id} cannot depend on itself.")
            if task.task_type in {TaskType.DEDICATED, TaskType.GENERAL, TaskType.UNIVERSAL}:
                if task.required_resource_count != 1:
                    errors.append(f"Task {task.id} must require exactly one resource.")
            if task.task_type == TaskType.DEDICATED and not task.required_specializations:
                errors.append(f"Dedicated task {task.id} must define required_specializations.")
            if task.task_type == TaskType.UNIVERSAL and task.required_specializations:
                errors.append(f"Universal task {task.id} cannot define required_specializations.")
            if task.task_type in {TaskType.COMMON_DEDICATED, TaskType.COMMON_GENERAL}:
                if task.required_resource_count < 2:
                    errors.append(f"Common task {task.id} must require at least two resources.")
                if len(task.required_specializations) > task.required_resource_count:
                    errors.append(f"Task {task.id} has more required specializations than required resources.")

    def _validate_dependencies(self, scenario: Scenario, tasks_by_id: dict[str, object], errors: list[str]) -> None:
        for task in scenario.tasks:
            for dependency_id in task.dependencies:
                if dependency_id not in tasks_by_id:
                    errors.append(f"Task {task.id} depends on missing task {dependency_id}.")

    def _validate_graph(self, scenario: Scenario, errors: list[str]) -> None:
        graph = nx.DiGraph()
        for task in scenario.tasks:
            graph.add_node(task.id)
            for dependency_id in task.dependencies:
                graph.add_edge(dependency_id, task.id)

        if not nx.is_directed_acyclic_graph(graph):
            errors.append("Task dependency graph must be acyclic.")

    def _validate_assignments(self, scenario: Scenario, errors: list[str]) -> None:
        for task in scenario.tasks:
            if not self.matcher.generate_assignments(task, scenario.resources):
                errors.append(f"Task {task.id} has no compatible resource assignment.")

    def _validate_unused_resources(self, scenario: Scenario, warnings: list[str]) -> None:
        used_resource_ids: set[str] = set()
        for task in scenario.tasks:
            for assignment in self.matcher.generate_assignments(task, scenario.resources):
                used_resource_ids.update(resource.id for resource in assignment)

        for resource in scenario.resources:
            if resource.id not in used_resource_ids:
                warnings.append(f"Resource {resource.id} is not compatible with any task.")
