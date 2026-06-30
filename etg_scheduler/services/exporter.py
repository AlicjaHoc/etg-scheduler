import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path

from etg_scheduler.models.schedule import ScheduleResult
from etg_scheduler.utilities.file_name_helper import safe_file_part, timestamp_suffix
from etg_scheduler.utilities.time_formatter import format_money, format_number, format_percent


@dataclass(frozen=True)
class ExportPaths:
    json_path: Path
    csv_path: Path
    report_path: Path


class ScheduleExporter:
    def __init__(self, output_dir: Path | str = "output") -> None:
        self.output_dir = Path(output_dir)

    def export(self, result: ScheduleResult) -> ExportPaths:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        base_name = f"{safe_file_part(result.scenario_name)}_{timestamp_suffix(result.created_at)}"
        json_path = self.output_dir / f"{base_name}_schedule.json"
        csv_path = self.output_dir / f"{base_name}_schedule.csv"
        report_path = self.output_dir / f"{base_name}_report.md"

        self._write_json(result, json_path)
        self._write_csv(result, csv_path)
        self._write_report(result, report_path)

        return ExportPaths(json_path=json_path, csv_path=csv_path, report_path=report_path)

    def _write_json(self, result: ScheduleResult, path: Path) -> None:
        with path.open("w", encoding="utf-8") as file:
            json.dump(self._plain_value(result), file, indent=2, ensure_ascii=False)

    def _plain_value(self, value):
        if hasattr(value, "__dataclass_fields__"):
            return self._plain_value(asdict(value))
        if isinstance(value, dict):
            return {key: self._plain_value(item) for key, item in value.items()}
        if isinstance(value, list):
            return [self._plain_value(item) for item in value]
        if isinstance(value, Enum):
            return value.value
        if isinstance(value, datetime):
            return value.isoformat(timespec="seconds")
        return value

    def _write_csv(self, result: ScheduleResult, path: Path) -> None:
        with path.open("w", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "task_id",
                    "task_name",
                    "task_type",
                    "start_time",
                    "finish_time",
                    "duration",
                    "resource_ids",
                    "resource_names",
                    "cost",
                ]
            )
            for task in result.scheduled_tasks:
                writer.writerow(
                    [
                        task.task_id,
                        task.task_name,
                        task.task_type.value,
                        format_number(task.start_time),
                        format_number(task.finish_time),
                        format_number(task.duration),
                        ";".join(task.assigned_resource_ids),
                        ";".join(task.assigned_resource_names),
                        format_money(task.cost),
                    ]
                )

    def _write_report(self, result: ScheduleResult, path: Path) -> None:
        lines = [
            f"# ETG schedule report - {result.scenario_name}",
            "",
            f"Generated at: {result.created_at.isoformat(timespec='seconds')}",
            f"Algorithm: {result.algorithm}",
            f"Mode: {result.optimization_mode.value}",
        ]
        if result.time_constraint is not None:
            lines.append(f"Time constraint: {format_number(result.time_constraint)}")
            if result.summary.total_execution_time <= result.time_constraint:
                lines.append("Constraint status: OK")
            else:
                over = result.summary.total_execution_time - result.time_constraint
                lines.append(f"Constraint status: over by {format_number(over)}")
        lines.extend(
            [
                "",
                "Scenario",
                "",
                result.scenario_description,
                "",
                "Summary",
                "",
                f"Total execution time: {format_number(result.summary.total_execution_time)}",
                f"Total cost: {format_money(result.summary.total_cost)}",
                f"Average resource utilization: {format_percent(result.summary.average_resource_utilization)}",
                "",
                "Schedule",
                "",
            ]
        )

        for task in result.scheduled_tasks:
            lines.append(
                f"{task.task_id} {task.task_name}: "
                f"{task.task_type.value}, "
                f"{format_number(task.start_time)} -> {format_number(task.finish_time)}, "
                f"{', '.join(task.assigned_resource_names)}, "
                f"cost {format_money(task.cost)}"
            )

        lines.extend(
            [
                "",
                "Resource usage",
                "",
            ]
        )

        for usage in result.summary.resource_usage:
            lines.append(
                f"{usage.resource_name}: "
                f"busy {format_number(usage.busy_time)}, "
                f"idle {format_number(usage.idle_time)}, "
                f"utilization {format_percent(usage.utilization)}, "
                f"tasks {usage.tasks_count}"
            )

        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
