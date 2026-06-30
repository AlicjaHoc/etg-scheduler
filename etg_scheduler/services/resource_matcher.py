from itertools import combinations

from etg_scheduler.models.enums import ResourceType, TaskType
from etg_scheduler.models.resource import Resource
from etg_scheduler.models.task import Task


class ResourceMatcher:
    def generate_assignments(self, task: Task, resources: list[Resource]) -> list[list[Resource]]:
        if task.task_type == TaskType.DEDICATED:
            return self._dedicated_assignments(task, resources)
        if task.task_type == TaskType.GENERAL:
            return self._general_assignments(task, resources)
        if task.task_type == TaskType.UNIVERSAL:
            return self._universal_assignments(resources)
        if task.task_type == TaskType.COMMON_DEDICATED:
            return self._common_dedicated_assignments(task, resources)
        if task.task_type == TaskType.COMMON_GENERAL:
            return self._common_general_assignments(task, resources)
        return []

    def _dedicated_assignments(self, task: Task, resources: list[Resource]) -> list[list[Resource]]:
        return [
            [resource]
            for resource in resources
            if resource.resource_type == ResourceType.SPECIALIZED
            and resource.specialization in task.required_specializations
        ]

    def _general_assignments(self, task: Task, resources: list[Resource]) -> list[list[Resource]]:
        if not task.required_specializations:
            return [[resource] for resource in resources]
        return [
            [resource]
            for resource in resources
            if resource.resource_type == ResourceType.UNIVERSAL
            or resource.specialization in task.required_specializations
        ]

    def _universal_assignments(self, resources: list[Resource]) -> list[list[Resource]]:
        return [[resource] for resource in resources if resource.resource_type == ResourceType.UNIVERSAL]

    def _common_dedicated_assignments(self, task: Task, resources: list[Resource]) -> list[list[Resource]]:
        specialized = [resource for resource in resources if resource.resource_type == ResourceType.SPECIALIZED]
        required_count = max(task.required_resource_count, len(task.required_specializations))
        return self._assign_multiple_resources(task.required_specializations, specialized, required_count)

    def _common_general_assignments(self, task: Task, resources: list[Resource]) -> list[list[Resource]]:
        required_count = max(task.required_resource_count, len(task.required_specializations))
        return self._assign_multiple_resources(task.required_specializations, resources, required_count)

    def _assign_multiple_resources(
        self,
        required_specializations: list[str],
        resources: list[Resource],
        required_count: int,
    ) -> list[list[Resource]]:
        if required_specializations:
            assignments = self._assign_required_specializations(required_specializations, resources)
        else:
            assignments = [[]]

        completed: list[list[Resource]] = []
        for assignment in assignments:
            remaining_resources = [resource for resource in resources if resource.id not in {item.id for item in assignment}]
            missing_count = required_count - len(assignment)
            if missing_count < 0:
                continue
            if missing_count == 0:
                completed.append(assignment)
                continue
            for extra_resources in combinations(remaining_resources, missing_count):
                completed.append(assignment + list(extra_resources))

        return self._unique_assignments(completed)

    def _assign_required_specializations(
        self,
        required_specializations: list[str],
        resources: list[Resource],
    ) -> list[list[Resource]]:
        assignments: list[list[Resource]] = []

        def backtrack(index: int, selected: list[Resource]) -> None:
            if index == len(required_specializations):
                assignments.append(selected.copy())
                return

            specialization = required_specializations[index]
            for resource in resources:
                if resource.id in {item.id for item in selected}:
                    continue
                if resource.specialization != specialization:
                    continue
                selected.append(resource)
                backtrack(index + 1, selected)
                selected.pop()

        backtrack(0, [])
        return assignments

    def _unique_assignments(self, assignments: list[list[Resource]]) -> list[list[Resource]]:
        seen: set[tuple[str, ...]] = set()
        unique: list[list[Resource]] = []
        for assignment in assignments:
            key = tuple(sorted(resource.id for resource in assignment))
            if key in seen:
                continue
            seen.add(key)
            unique.append(assignment)
        return unique
