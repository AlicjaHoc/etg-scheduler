from __future__ import annotations

import json
from pathlib import Path

from etg_scheduler.models.scenario import Scenario


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

        return Scenario.model_validate(data)
