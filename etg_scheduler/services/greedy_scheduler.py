from __future__ import annotations

from dataclasses import dataclass

from etg_scheduler.models.enums import OptimizationMode
from etg_scheduler.models.resource import Resource
from etg_scheduler.models.scenario import Scenario
from etg_scheduler.models.schedule import ResourceUsage, ScheduledTask, ScheduleResult, ScheduleSummary
from etg_scheduler.models.task import Task
from etg_scheduler.services.cost_calculator import CostCalculator
from etg_scheduler.services.resource_matcher import ResourceMatcher


@dataclass(frozen=True)
class ScheduleCandidate:
    task: Task
    resources: list[Resource]
    start_time: float
    finish_time: float
    duration: float
    cost: float


class GreedyScheduler:
    def __init__(self, matcher: ResourceMatcher | None = None, cost_calculator: CostCalculator | None = None) -> None:
        self.matcher = matcher or ResourceMatcher()
        self.cost_calculator = cost_calculator or CostCalculator()

    def schedule(self, scenario: Scenario, mode: OptimizationMode) -> ScheduleResult:
        remaining_tasks = {task.id: task for task in scenario.tasks}
        scheduled_by_id: dict[str, ScheduledTask] = {}
        resource_available_at = {resource.id: 0.0 for resource in scenario.resources}
        scheduled_tasks: list[ScheduledTask] = []

        while remaining_tasks:
            ready_tasks = [
                task
                for task in remaining_tasks.values()
                if all(dependency_id in scheduled_by_id for dependency_id in task.dependencies)
            ]
            if not ready_tasks:
                raise RuntimeError("Scheduling stopped because no ready tasks are available.")

            candidates = self._build_candidates(ready_tasks, scenario.resources, scheduled_by_id, resource_available_at)
            if not candidates:
                raise RuntimeError("Scheduling stopped because ready tasks have no compatible resources.")

            selected = self._select_candidate(candidates, mode)
            scheduled_task = self._to_scheduled_task(selected)
            scheduled_tasks.append(scheduled_task)
            scheduled_by_id[scheduled_task.task_id] = scheduled_task
            del remaining_tasks[scheduled_task.task_id]

            for resource in selected.resources:
                resource_available_at[resource.id] = selected.finish_time

        summary = self._build_summary(scenario, scheduled_tasks, mode)
        return ScheduleResult(
            scenario_name=scenario.name,
            scenario_description=scenario.description,
            optimization_mode=mode,
            scheduled_tasks=scheduled_tasks,
            summary=summary,
        )

    def _build_candidates(
        self,
        ready_tasks: list[Task],
        resources: list[Resource],
        scheduled_by_id: dict[str, ScheduledTask],
        resource_available_at: dict[str, float],
    ) -> list[ScheduleCandidate]:
        candidates: list[ScheduleCandidate] = []
        for task in ready_tasks:
            dependency_finish_time = max(
                (scheduled_by_id[dependency_id].finish_time for dependency_id in task.dependencies),
                default=0.0,
            )
            for assignment in self.matcher.generate_assignments(task, resources):
                resource_ready_time = max(resource_available_at[resource.id] for resource in assignment)
                start_time = max(dependency_finish_time, resource_ready_time)
                duration = self.cost_calculator.adjusted_duration(task, assignment)
                finish_time = start_time + duration
                cost = self.cost_calculator.task_cost(task, assignment, duration)
                candidates.append(
                    ScheduleCandidate(
                        task=task,
                        resources=assignment,
                        start_time=start_time,
                        finish_time=finish_time,
                        duration=duration,
                        cost=cost,
                    )
                )
        return candidates

    def _select_candidate(self, candidates: list[ScheduleCandidate], mode: OptimizationMode) -> ScheduleCandidate:
        if mode == OptimizationMode.MINIMIZE_TIME:
            return min(candidates, key=lambda candidate: self._time_key(candidate))
        if mode == OptimizationMode.MINIMIZE_COST:
            return min(candidates, key=lambda candidate: self._cost_key(candidate))
        return min(candidates, key=lambda candidate: self._balanced_key(candidate, candidates))

    def _time_key(self, candidate: ScheduleCandidate) -> tuple[float, float, float, str]:
        return (candidate.finish_time, candidate.start_time, candidate.cost, candidate.task.id)

    def _cost_key(self, candidate: ScheduleCandidate) -> tuple[float, float, float, str]:
        return (candidate.cost, candidate.finish_time, candidate.start_time, candidate.task.id)

    def _balanced_key(
        self,
        candidate: ScheduleCandidate,
        candidates: list[ScheduleCandidate],
    ) -> tuple[float, float, float, str]:
        max_finish_time = max(item.finish_time for item in candidates) or 1.0
        max_cost = max(item.cost for item in candidates) or 1.0
        score = 0.6 * (candidate.finish_time / max_finish_time) + 0.4 * (candidate.cost / max_cost)
        return (score, candidate.finish_time, candidate.cost, candidate.task.id)

    def _to_scheduled_task(self, candidate: ScheduleCandidate) -> ScheduledTask:
        return ScheduledTask(
            task_id=candidate.task.id,
            task_name=candidate.task.name,
            task_type=candidate.task.task_type,
            start_time=candidate.start_time,
            finish_time=candidate.finish_time,
            duration=candidate.duration,
            assigned_resource_ids=[resource.id for resource in candidate.resources],
            assigned_resource_names=[resource.name for resource in candidate.resources],
            cost=candidate.cost,
        )

    def _build_summary(
        self,
        scenario: Scenario,
        scheduled_tasks: list[ScheduledTask],
        mode: OptimizationMode,
    ) -> ScheduleSummary:
        total_execution_time = max((task.finish_time for task in scheduled_tasks), default=0.0)
        total_cost = sum(task.cost for task in scheduled_tasks)
        usage_items: list[ResourceUsage] = []

        for resource in scenario.resources:
            tasks_for_resource = [
                task for task in scheduled_tasks if resource.id in task.assigned_resource_ids
            ]
            busy_time = sum(task.duration for task in tasks_for_resource)
            idle_time = max(total_execution_time - busy_time, 0.0)
            utilization = busy_time / total_execution_time if total_execution_time else 0.0
            usage_items.append(
                ResourceUsage(
                    resource_id=resource.id,
                    resource_name=resource.name,
                    busy_time=busy_time,
                    idle_time=idle_time,
                    utilization=utilization,
                    tasks_count=len(tasks_for_resource),
                )
            )

        average_utilization = (
            sum(item.utilization for item in usage_items) / len(usage_items)
            if usage_items
            else 0.0
        )

        return ScheduleSummary(
            scenario_name=scenario.name,
            optimization_mode=mode,
            total_execution_time=total_execution_time,
            total_cost=total_cost,
            average_resource_utilization=average_utilization,
            resource_usage=usage_items,
        )
