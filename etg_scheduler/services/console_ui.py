from pathlib import Path

from etg_scheduler.models.enums import OptimizationMode
from etg_scheduler.models.resource import Resource
from etg_scheduler.models.scenario import Scenario
from etg_scheduler.models.schedule import ScheduleResult
from etg_scheduler.models.task import Task
from etg_scheduler.models.validation import ValidationResult
from etg_scheduler.services.exporter import ExportPaths
from etg_scheduler.utilities.time_formatter import format_money, format_number, format_percent


class ConsoleUI:
    def show_title(self) -> None:
        print()
        print("ETG Scheduler")
        print("Simple Extended Task Graph scheduler")

    def choose_scenario(self, scenario_paths: list[Path]) -> Path:
        if not scenario_paths:
            raise FileNotFoundError("No scenario JSON files found in the scenarios folder.")

        self._section("Scenarios")
        for index, path in enumerate(scenario_paths, start=1):
            print(f"{index}. {path}")

        selected = self._ask_number("Choose scenario", 1, len(scenario_paths))
        return scenario_paths[selected - 1]

    def choose_mode(self, default_mode: OptimizationMode) -> OptimizationMode:
        modes = list(OptimizationMode)
        default_index = modes.index(default_mode) + 1

        self._section("Modes")
        for index, mode in enumerate(modes, start=1):
            if mode == default_mode:
                print(f"{index}. {mode.value} default")
            else:
                print(f"{index}. {mode.value}")

        selected = self._ask_number("Choose mode", 1, len(modes), default_index)
        return modes[selected - 1]

    def show_scenario_summary(
        self,
        scenario: Scenario,
        path: Path,
        mode: OptimizationMode,
        algorithm: str,
        time_constraint: float | None,
    ) -> None:
        self._section("Scenario")
        print(f"Name: {scenario.name}")
        print(f"File: {path}")
        print(f"Mode: {mode.value}")
        print(f"Algorithm: {algorithm}")
        if time_constraint is not None:
            print(f"Time constraint: {format_number(time_constraint)}")
        print(f"Tasks: {len(scenario.tasks)}")
        print(f"Resources: {len(scenario.resources)}")
        print(scenario.description)

    def show_tasks(self, tasks: list[Task]) -> None:
        self._section("Tasks")
        print("id | type | duration | depends on | resources | specializations | name")
        for task in tasks:
            dependencies = ", ".join(task.dependencies) or "-"
            specializations = ", ".join(task.required_specializations) or "-"
            print(
                f"{task.id} | {task.task_type.value} | {format_number(task.duration)} | "
                f"{dependencies} | {task.required_resource_count} | {specializations} | {task.name}"
            )

    def show_resources(self, resources: list[Resource]) -> None:
        self._section("Resources")
        print("id | type | specialization | cost | speed | name")
        for resource in resources:
            specialization = resource.specialization or "-"
            print(
                f"{resource.id} | {resource.resource_type.value} | {specialization} | "
                f"{format_money(resource.cost_per_time_unit)} | {format_number(resource.speed_multiplier)} | {resource.name}"
            )

    def show_validation(self, result: ValidationResult) -> None:
        self._section("Validation")
        if result.is_valid:
            print("OK")
        else:
            for error in result.errors:
                print(f"ERROR: {error}")

        for warning in result.warnings:
            print(f"WARNING: {warning}")

    def show_schedule(self, result: ScheduleResult) -> None:
        self._section("Schedule")
        print("task | type | start | finish | resources | cost")
        for task in result.scheduled_tasks:
            print(
                f"{task.task_id} {task.task_name} | {task.task_type.value} | "
                f"{format_number(task.start_time)} | {format_number(task.finish_time)} | "
                f"{', '.join(task.assigned_resource_names)} | {format_money(task.cost)}"
            )
        self._show_summary(result)

    def _show_summary(self, result: ScheduleResult) -> None:
        self._section("Summary")
        print(f"Algorithm: {result.algorithm}")
        if result.time_constraint is not None:
            print(f"Time constraint: {format_number(result.time_constraint)}")
            if result.summary.total_execution_time <= result.time_constraint:
                print("Constraint status: OK")
            else:
                over = result.summary.total_execution_time - result.time_constraint
                print(f"Constraint status: over by {format_number(over)}")
        print(f"Total time: {format_number(result.summary.total_execution_time)}")
        print(f"Total cost: {format_money(result.summary.total_cost)}")
        print(f"Average utilization: {format_percent(result.summary.average_resource_utilization)}")

        print()
        print("Resource usage")
        print("resource | busy | idle | utilization | tasks")
        for usage in result.summary.resource_usage:
            print(
                f"{usage.resource_name} | {format_number(usage.busy_time)} | "
                f"{format_number(usage.idle_time)} | {format_percent(usage.utilization)} | {usage.tasks_count}"
            )

    def show_timeline(self, result: ScheduleResult) -> None:
        self._section("Timeline")
        for usage in result.summary.resource_usage:
            segments = []
            for task in result.scheduled_tasks:
                if usage.resource_id in task.assigned_resource_ids:
                    segments.append(f"{format_number(task.start_time)}-{format_number(task.finish_time)} {task.task_id}")
            print(f"{usage.resource_name}: {'; '.join(segments) or '-'}")

    def show_exports(self, paths: ExportPaths) -> None:
        self._section("Files")
        print(paths.json_path)
        print(paths.csv_path)
        print(paths.report_path)

    def show_error(self, message: str) -> None:
        print()
        print(f"ERROR: {message}")

    def _section(self, title: str) -> None:
        print()
        print(title)

    def _ask_number(self, prompt: str, minimum: int, maximum: int, default: int | None = None) -> int:
        while True:
            if default is None:
                value = input(f"{prompt}: ").strip()
            else:
                value = input(f"{prompt} [{default}]: ").strip()
            if not value and default is not None:
                return default
            if value.isdigit():
                selected = int(value)
                if minimum <= selected <= maximum:
                    return selected
            print(f"Enter a number from {minimum} to {maximum}.")
