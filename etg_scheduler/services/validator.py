from etg_scheduler.models.enums import ResourceType, TaskType
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

        self._validate_scenario(scenario, errors)

        if len(tasks_by_id) != len(scenario.tasks):
            errors.append("Task IDs must be unique.")
        if len(resources_by_id) != len(scenario.resources):
            errors.append("Resource IDs must be unique.")

        self._validate_tasks(scenario, errors)
        self._validate_resources(scenario, errors)
        self._validate_dependencies(scenario, tasks_by_id, errors)
        self._validate_graph(scenario, errors)
        self._validate_assignments(scenario, errors)
        self._validate_unused_resources(scenario, warnings)

        return ValidationResult(errors=errors, warnings=warnings)

    def _validate_scenario(self, scenario: Scenario, errors: list[str]) -> None:
        if not scenario.name.strip():
            errors.append("Scenario name cannot be empty.")
        if not scenario.description.strip():
            errors.append("Scenario description cannot be empty.")
        if not scenario.tasks:
            errors.append("Scenario must contain at least one task.")
        if not scenario.resources:
            errors.append("Scenario must contain at least one resource.")
        if scenario.time_constraint is not None and scenario.time_constraint <= 0:
            errors.append("Scenario time constraint must be greater than zero.")

    def _validate_tasks(self, scenario: Scenario, errors: list[str]) -> None:
        for task in scenario.tasks:
            if not task.id.strip():
                errors.append("Task ID cannot be empty.")
            if not task.name.strip():
                errors.append(f"Task {task.id} name cannot be empty.")
            if task.duration <= 0:
                errors.append(f"Task {task.id} duration must be greater than zero.")
            if task.required_resource_count < 1:
                errors.append(f"Task {task.id} must require at least one resource.")
            if task.base_cost < 0:
                errors.append(f"Task {task.id} base cost cannot be negative.")
            if "" in [value.strip() for value in task.dependencies]:
                errors.append(f"Task {task.id} has an empty dependency ID.")
            if "" in [value.strip() for value in task.required_specializations]:
                errors.append(f"Task {task.id} has an empty specialization.")

            self._validate_task_type_rules(task, errors)

    def _validate_task_type_rules(self, task, errors: list[str]) -> None:
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

    def _validate_resources(self, scenario: Scenario, errors: list[str]) -> None:
        for resource in scenario.resources:
            if not resource.id.strip():
                errors.append("Resource ID cannot be empty.")
            if not resource.name.strip():
                errors.append(f"Resource {resource.id} name cannot be empty.")
            if resource.cost_per_time_unit < 0:
                errors.append(f"Resource {resource.id} cost cannot be negative.")
            if resource.speed_multiplier <= 0:
                errors.append(f"Resource {resource.id} speed multiplier must be greater than zero.")
            if resource.resource_type == ResourceType.SPECIALIZED and not resource.specialization:
                errors.append(f"Specialized resource {resource.id} must define specialization.")
            if resource.resource_type == ResourceType.UNIVERSAL and resource.specialization:
                errors.append(f"Universal resource {resource.id} cannot define specialization.")

    def _validate_dependencies(self, scenario: Scenario, tasks_by_id: dict[str, object], errors: list[str]) -> None:
        for task in scenario.tasks:
            for dependency_id in task.dependencies:
                if dependency_id not in tasks_by_id:
                    errors.append(f"Task {task.id} depends on missing task {dependency_id}.")

    def _validate_graph(self, scenario: Scenario, errors: list[str]) -> None:
        graph = {task.id: task.dependencies for task in scenario.tasks}
        visited: set[str] = set()
        active: set[str] = set()

        def visit(task_id: str) -> bool:
            if task_id in active:
                return True
            if task_id in visited:
                return False
            active.add(task_id)
            for dependency_id in graph.get(task_id, []):
                if dependency_id in graph and visit(dependency_id):
                    return True
            active.remove(task_id)
            visited.add(task_id)
            return False

        for task_id in graph:
            if visit(task_id):
                errors.append("Task dependency graph must be acyclic.")
                return

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
