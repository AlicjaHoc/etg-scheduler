from __future__ import annotations

from pathlib import Path
from textwrap import shorten

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
        print("Extended Task Graph scheduling project")
        print("=" * 45)

    def choose_scenario(self, scenario_paths: list[Path]) -> Path:
        if not scenario_paths:
            raise FileNotFoundError("No scenario JSON files found in the scenarios folder.")

        self._section("Available scenarios")
        for index, path in enumerate(scenario_paths, start=1):
            print(f"{index}. {path.stem} ({path})")

        selected = self._ask_number("Choose scenario", 1, len(scenario_paths))
        return scenario_paths[selected - 1]

    def choose_mode(self, default_mode: OptimizationMode) -> OptimizationMode:
        modes = list(OptimizationMode)
        default_index = modes.index(default_mode) + 1

        self._section("Optimization modes")
        for index, mode in enumerate(modes, start=1):
            marker = " default" if mode == default_mode else ""
            print(f"{index}. {mode.value}{marker}")

        selected = self._ask_number("Choose optimization mode", 1, len(modes), default_index)
        return modes[selected - 1]

    def show_scenario_summary(self, scenario: Scenario, path: Path, mode: OptimizationMode) -> None:
        self._section("Scenario")
        print(f"Name: {scenario.name}")
        print(f"Description: {scenario.description}")
        print(f"File: {path}")
        print(f"Tasks: {len(scenario.tasks)}")
        print(f"Resources: {len(scenario.resources)}")
        print(f"Optimization mode: {mode.value}")

    def show_tasks(self, tasks: list[Task]) -> None:
        self._section("Tasks")
        rows = [
            [
                task.id,
                task.name,
                task.task_type.value,
                format_number(task.duration),
                ", ".join(task.dependencies) or "-",
                str(task.required_resource_count),
                ", ".join(task.required_specializations) or "-",
            ]
            for task in tasks
        ]
        self._print_table(
            ["ID", "Name", "Type", "Dur", "Deps", "Res", "Specializations"],
            rows,
            [8, 24, 5, 6, 12, 4, 24],
        )

    def show_resources(self, resources: list[Resource]) -> None:
        self._section("Resources")
        rows = [
            [
                resource.id,
                resource.name,
                resource.resource_type.value,
                resource.specialization or "-",
                format_money(resource.cost_per_time_unit),
                format_number(resource.speed_multiplier),
            ]
            for resource in resources
        ]
        self._print_table(
            ["ID", "Name", "Type", "Specialization", "Cost", "Speed"],
            rows,
            [18, 24, 12, 18, 8, 7],
        )

    def show_validation(self, result: ValidationResult) -> None:
        self._section("Validation")
        if result.is_valid:
            print("OK - scenario is valid.")
        else:
            print("Errors:")
            for error in result.errors:
                print(f"- {error}")

        if result.warnings:
            print("Warnings:")
            for warning in result.warnings:
                print(f"- {warning}")

    def show_schedule(self, result: ScheduleResult) -> None:
        self._section("Final schedule")
        rows = [
            [
                f"{task.task_id} {task.task_name}",
                task.task_type.value,
                format_number(task.start_time),
                format_number(task.finish_time),
                format_number(task.duration),
                ", ".join(task.assigned_resource_names),
                format_money(task.cost),
            ]
            for task in result.scheduled_tasks
        ]
        self._print_table(
            ["Task", "Type", "Start", "Finish", "Dur", "Resources", "Cost"],
            rows,
            [28, 5, 8, 8, 7, 32, 10],
        )
        self._show_summary(result)

    def _show_summary(self, result: ScheduleResult) -> None:
        summary = result.summary
        self._section("Summary")
        print(f"Total execution time: {format_number(summary.total_execution_time)}")
        print(f"Total cost: {format_money(summary.total_cost)}")
        print(f"Average resource utilization: {format_percent(summary.average_resource_utilization)}")

        print()
        print("Resource utilization:")
        rows = [
            [
                usage.resource_name,
                format_number(usage.busy_time),
                format_number(usage.idle_time),
                format_percent(usage.utilization),
                str(usage.tasks_count),
            ]
            for usage in summary.resource_usage
        ]
        self._print_table(
            ["Resource", "Busy", "Idle", "Util", "Tasks"],
            rows,
            [28, 8, 8, 8, 6],
        )

    def show_timeline(self, result: ScheduleResult) -> None:
        self._section("Timeline by resource")
        for usage in result.summary.resource_usage:
            segments = []
            for task in result.scheduled_tasks:
                if usage.resource_id in task.assigned_resource_ids:
                    segments.append(f"{format_number(task.start_time)}-{format_number(task.finish_time)} {task.task_id}")
            timeline = " | ".join(segments) or "-"
            print(f"{usage.resource_name}: {timeline}")

    def show_exports(self, paths: ExportPaths) -> None:
        self._section("Exported files")
        print(f"JSON: {paths.json_path}")
        print(f"CSV: {paths.csv_path}")
        print(f"Report: {paths.report_path}")

    def show_error(self, message: str) -> None:
        print()
        print("ERROR")
        print(message)

    def _section(self, title: str) -> None:
        print()
        print(title)
        print("-" * len(title))

    def _ask_number(self, prompt: str, minimum: int, maximum: int, default: int | None = None) -> int:
        while True:
            suffix = f" [{default}]" if default is not None else ""
            value = input(f"{prompt}{suffix}: ").strip()
            if not value and default is not None:
                return default
            if not value.isdigit():
                print("Please enter a number.")
                continue
            selected = int(value)
            if minimum <= selected <= maximum:
                return selected
            print(f"Please choose a number from {minimum} to {maximum}.")

    def _print_table(self, headers: list[str], rows: list[list[str]], widths: list[int]) -> None:
        header_line = "  ".join(self._fit(header, width) for header, width in zip(headers, widths))
        divider = "  ".join("-" * width for width in widths)
        print(header_line)
        print(divider)
        for row in rows:
            print("  ".join(self._fit(value, width) for value, width in zip(row, widths)))

    def _fit(self, value: str, width: int) -> str:
        return shorten(str(value), width=width, placeholder="...").ljust(width)
