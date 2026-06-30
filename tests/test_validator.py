from etg_scheduler.models.enums import OptimizationMode, ResourceType, TaskType
from etg_scheduler.models.resource import Resource
from etg_scheduler.models.scenario import Scenario
from etg_scheduler.models.task import Task
from etg_scheduler.services.validator import ScenarioValidator


def universal_resource(resource_id: str = "u1") -> Resource:
    return Resource(
        id=resource_id,
        name="Universal worker",
        resource_type=ResourceType.UNIVERSAL,
        cost_per_time_unit=10,
        speed_multiplier=1,
    )


def doctor_resource(resource_id: str = "d1") -> Resource:
    return Resource(
        id=resource_id,
        name="Doctor",
        resource_type=ResourceType.SPECIALIZED,
        specialization="Doctor",
        cost_per_time_unit=40,
        speed_multiplier=1,
    )


def scenario_with(tasks: list[Task], resources: list[Resource]) -> Scenario:
    return Scenario(
        name="Test scenario",
        description="Small validation scenario",
        tasks=tasks,
        resources=resources,
        default_optimization_mode=OptimizationMode.BALANCED,
    )


def test_validator_accepts_valid_scenario() -> None:
    scenario = scenario_with(
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
        ],
        resources=[universal_resource(), doctor_resource()],
    )

    result = ScenarioValidator().validate(scenario)

    assert result.is_valid
    assert result.errors == []


def test_validator_rejects_missing_dependency() -> None:
    scenario = scenario_with(
        tasks=[
            Task(id="a", name="Register", task_type=TaskType.GENERAL, duration=1, dependencies=["missing"]),
        ],
        resources=[universal_resource()],
    )

    result = ScenarioValidator().validate(scenario)

    assert not result.is_valid
    assert "Task a depends on missing task missing." in result.errors


def test_validator_rejects_cycle() -> None:
    scenario = scenario_with(
        tasks=[
            Task(id="a", name="A", task_type=TaskType.GENERAL, duration=1, dependencies=["b"]),
            Task(id="b", name="B", task_type=TaskType.GENERAL, duration=1, dependencies=["a"]),
        ],
        resources=[universal_resource()],
    )

    result = ScenarioValidator().validate(scenario)

    assert not result.is_valid
    assert "Task dependency graph must be acyclic." in result.errors


def test_validator_rejects_impossible_assignment() -> None:
    scenario = scenario_with(
        tasks=[
            Task(
                id="a",
                name="Specialist work",
                task_type=TaskType.DEDICATED,
                duration=1,
                required_specializations=["Surgeon"],
            ),
        ],
        resources=[universal_resource(), doctor_resource()],
    )

    result = ScenarioValidator().validate(scenario)

    assert not result.is_valid
    assert "Task a has no compatible resource assignment." in result.errors
