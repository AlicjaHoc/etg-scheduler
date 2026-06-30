import random
from dataclasses import dataclass

from etg_scheduler.models.enums import OptimizationMode
from etg_scheduler.models.resource import Resource
from etg_scheduler.models.scenario import Scenario
from etg_scheduler.models.schedule import ResourceUsage, ScheduledTask, ScheduleResult, ScheduleSummary
from etg_scheduler.models.task import Task
from etg_scheduler.services.resource_matcher import ResourceMatcher


@dataclass
class Chromosome:
    choices: dict[str, int]
    priorities: dict[str, float]


class GeneticScheduler:
    def __init__(
        self,
        matcher: ResourceMatcher | None = None,
        population_size: int = 40,
        generations: int = 80,
        mutation_rate: float = 0.15,
        seed: int = 7,
    ) -> None:
        self.matcher = matcher or ResourceMatcher()
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.random = random.Random(seed)

    def schedule(self, scenario: Scenario, time_constraint: float) -> ScheduleResult:
        assignments = {
            task.id: self.matcher.generate_assignments(task, scenario.resources)
            for task in scenario.tasks
        }
        population = [self._random_chromosome(scenario, assignments) for _ in range(self.population_size)]
        best = min(population, key=lambda item: self._score(scenario, assignments, item, time_constraint))

        for _ in range(self.generations):
            ranked = sorted(population, key=lambda item: self._score(scenario, assignments, item, time_constraint))
            if self._score(scenario, assignments, ranked[0], time_constraint) < self._score(
                scenario,
                assignments,
                best,
                time_constraint,
            ):
                best = ranked[0]

            next_population = ranked[:4]
            while len(next_population) < self.population_size:
                parent_a = self._pick_parent(ranked)
                parent_b = self._pick_parent(ranked)
                child = self._crossover(parent_a, parent_b)
                self._mutate(child, assignments)
                next_population.append(child)
            population = next_population

        return self._build_schedule(scenario, assignments, best, time_constraint)

    def _random_chromosome(
        self,
        scenario: Scenario,
        assignments: dict[str, list[list[Resource]]],
    ) -> Chromosome:
        choices = {}
        priorities = {}
        for task in scenario.tasks:
            choices[task.id] = self.random.randrange(len(assignments[task.id]))
            priorities[task.id] = self.random.random()
        return Chromosome(choices=choices, priorities=priorities)

    def _pick_parent(self, ranked: list[Chromosome]) -> Chromosome:
        limit = max(2, len(ranked) // 3)
        return ranked[self.random.randrange(limit)]

    def _crossover(self, parent_a: Chromosome, parent_b: Chromosome) -> Chromosome:
        choices = {}
        priorities = {}
        for task_id in parent_a.choices:
            if self.random.random() < 0.5:
                choices[task_id] = parent_a.choices[task_id]
                priorities[task_id] = parent_a.priorities[task_id]
            else:
                choices[task_id] = parent_b.choices[task_id]
                priorities[task_id] = parent_b.priorities[task_id]
        return Chromosome(choices=choices, priorities=priorities)

    def _mutate(self, chromosome: Chromosome, assignments: dict[str, list[list[Resource]]]) -> None:
        for task_id in chromosome.choices:
            if self.random.random() < self.mutation_rate:
                chromosome.choices[task_id] = self.random.randrange(len(assignments[task_id]))
            if self.random.random() < self.mutation_rate:
                chromosome.priorities[task_id] = self.random.random()

    def _score(
        self,
        scenario: Scenario,
        assignments: dict[str, list[list[Resource]]],
        chromosome: Chromosome,
        time_constraint: float,
    ) -> float:
        result = self._build_schedule(scenario, assignments, chromosome, time_constraint)
        overtime = max(0, result.summary.total_execution_time - time_constraint)
        return result.summary.total_cost + overtime * 100000

    def _build_schedule(
        self,
        scenario: Scenario,
        assignments: dict[str, list[list[Resource]]],
        chromosome: Chromosome,
        time_constraint: float,
    ) -> ScheduleResult:
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

            task = min(ready_tasks, key=lambda item: chromosome.priorities[item.id])
            task_assignments = assignments[task.id]
            selected_resources = task_assignments[chromosome.choices[task.id] % len(task_assignments)]
            dependency_finish_time = max(
                (scheduled_by_id[dependency_id].finish_time for dependency_id in task.dependencies),
                default=0.0,
            )
            resource_ready_time = max(resource_available_at[resource.id] for resource in selected_resources)
            start_time = max(dependency_finish_time, resource_ready_time)
            duration = self._adjusted_duration(task, selected_resources)
            finish_time = start_time + duration
            cost = self._task_cost(task, selected_resources, duration)

            scheduled_task = ScheduledTask(
                task_id=task.id,
                task_name=task.name,
                task_type=task.task_type,
                start_time=start_time,
                finish_time=finish_time,
                duration=duration,
                assigned_resource_ids=[resource.id for resource in selected_resources],
                assigned_resource_names=[resource.name for resource in selected_resources],
                cost=cost,
            )
            scheduled_tasks.append(scheduled_task)
            scheduled_by_id[task.id] = scheduled_task
            del remaining_tasks[task.id]

            for resource in selected_resources:
                resource_available_at[resource.id] = finish_time

        summary = self._build_summary(scenario, scheduled_tasks)
        return ScheduleResult(
            scenario_name=scenario.name,
            scenario_description=scenario.description,
            optimization_mode=OptimizationMode.MINIMIZE_COST,
            scheduled_tasks=scheduled_tasks,
            summary=summary,
            algorithm="Genetic",
            time_constraint=time_constraint,
        )

    def _adjusted_duration(self, task: Task, resources: list[Resource]) -> float:
        average_speed = sum(resource.speed_multiplier for resource in resources) / len(resources)
        return task.duration / average_speed

    def _task_cost(self, task: Task, resources: list[Resource], duration: float) -> float:
        return sum(resource.cost_per_time_unit for resource in resources) * duration + task.base_cost

    def _build_summary(self, scenario: Scenario, scheduled_tasks: list[ScheduledTask]) -> ScheduleSummary:
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
            optimization_mode=OptimizationMode.MINIMIZE_COST,
            total_execution_time=total_execution_time,
            total_cost=total_cost,
            average_resource_utilization=average_utilization,
            resource_usage=usage_items,
        )
