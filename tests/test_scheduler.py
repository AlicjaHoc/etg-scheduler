import pytest

from etg_scheduler.models.enums import OptimizationMode, ResourceType, TaskType
from etg_scheduler.models.resource import Resource
from etg_scheduler.models.scenario import Scenario
from etg_scheduler.models.task import Task
from etg_scheduler.services.greedy_scheduler import GreedyScheduler
from etg_scheduler.services.scenario_loader import ScenarioLoader
from etg_scheduler.services.validator import ScenarioValidator


def simple_scenario() -> Scenario:
    return Scenario(
        name="Scheduler test",
        description="Small scheduling scenario",
        default_optimization_mode=OptimizationMode.MINIMIZE_TIME,
        resources=[
            Resource(
                id="u1",
                name="Universal worker",
                resource_type=ResourceType.UNIVERSAL,
                cost_per_time_unit=10,
                speed_multiplier=1,
            ),
            Resource(
                id="doctor",
                name="Doctor",
                resource_type=ResourceType.SPECIALIZED,
                specialization="Doctor",
                cost_per_time_unit=50,
                speed_multiplier=1,
            ),
        ],
        tasks=[
            Task(id="a", name="Register", task_type=TaskType.GENERAL, duration=1),
            Task(
                id="b",
                name="Examine",
                task_type=TaskType.DEDICATED,
                duration=2,
                dependencies=["a"],
                required_specializations=["Doctor"],
            ),
            Task(id="c", name="Archive", task_type=TaskType.UNIVERSAL, duration=1, dependencies=["b"]),
        ],
    )


def test_scheduler_respects_dependencies() -> None:
    result = GreedyScheduler().schedule(simple_scenario(), OptimizationMode.MINIMIZE_TIME)
    by_id = {task.task_id: task for task in result.scheduled_tasks}

    assert by_id["b"].start_time >= by_id["a"].finish_time
    assert by_id["c"].start_time >= by_id["b"].finish_time
    assert result.summary.total_execution_time == pytest.approx(by_id["c"].finish_time)


def test_scheduler_reports_cost_and_utilization() -> None:
    result = GreedyScheduler().schedule(simple_scenario(), OptimizationMode.BALANCED)

    assert result.summary.total_cost > 0
    assert 0 < result.summary.average_resource_utilization <= 1
    assert len(result.summary.resource_usage) == 2


def test_all_example_scenarios_are_valid_and_schedulable() -> None:
    loader = ScenarioLoader()
    validator = ScenarioValidator()
    scheduler = GreedyScheduler()

    for scenario_path in loader.list_scenarios():
        scenario = loader.load(scenario_path)
        validation = validator.validate(scenario)
        result = scheduler.schedule(scenario, scenario.default_optimization_mode)

        assert validation.is_valid, validation.errors
        assert len(result.scheduled_tasks) == len(scenario.tasks)
        assert result.summary.total_execution_time > 0
