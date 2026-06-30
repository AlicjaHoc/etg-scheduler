import argparse
from pathlib import Path

from etg_scheduler.models.enums import OptimizationMode
from etg_scheduler.services.console_ui import ConsoleUI
from etg_scheduler.services.exporter import ScheduleExporter
from etg_scheduler.services.genetic_scheduler import GeneticScheduler
from etg_scheduler.services.greedy_scheduler import GreedyScheduler
from etg_scheduler.services.resource_matcher import ResourceMatcher
from etg_scheduler.services.scenario_loader import ScenarioLoader
from etg_scheduler.services.validator import ScenarioValidator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m etg_scheduler",
        description="Extended Task Graph scheduling console application",
    )
    parser.add_argument("--scenario", help="Path to a scenario JSON file")
    parser.add_argument(
        "--mode",
        choices=[mode.value for mode in OptimizationMode],
        help="Optimization mode",
    )
    parser.add_argument("--algorithm", choices=["greedy", "genetic"], help="Scheduling algorithm")
    parser.add_argument("--time-constraint", type=float, help="Maximum allowed total execution time")
    parser.add_argument("--population", type=int, default=40, help="Genetic algorithm population size")
    parser.add_argument("--generations", type=int, default=80, help="Genetic algorithm generations")
    return parser


def main(argv: list[str] | None = None) -> int:
    ui = ConsoleUI()
    loader = ScenarioLoader()
    matcher = ResourceMatcher()
    validator = ScenarioValidator(matcher)
    exporter = ScheduleExporter()
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        ui.show_title()
        scenario_path = Path(args.scenario) if args.scenario else ui.choose_scenario(loader.list_scenarios())
        scenario = loader.load(scenario_path)
        if args.mode:
            mode = OptimizationMode(args.mode)
        elif args.scenario:
            mode = scenario.default_optimization_mode
        else:
            mode = ui.choose_mode(scenario.default_optimization_mode)
        time_constraint = args.time_constraint if args.time_constraint is not None else scenario.time_constraint
        algorithm = args.algorithm or ("genetic" if time_constraint is not None else "greedy")

        ui.show_scenario_summary(scenario, scenario_path, mode, algorithm, time_constraint)
        ui.show_tasks(scenario.tasks)
        ui.show_resources(scenario.resources)

        validation = validator.validate(scenario)
        ui.show_validation(validation)
        if not validation.is_valid:
            return 1

        if algorithm == "genetic":
            if time_constraint is None:
                raise ValueError("Genetic scheduling requires --time-constraint or scenario time_constraint.")
            scheduler = GeneticScheduler(matcher, population_size=args.population, generations=args.generations)
            result = scheduler.schedule(scenario, time_constraint)
        else:
            scheduler = GreedyScheduler(matcher)
            result = scheduler.schedule(scenario, mode)

        ui.show_schedule(result)
        ui.show_timeline(result)
        export_paths = exporter.export(result)
        ui.show_exports(export_paths)
        return 0
    except KeyboardInterrupt:
        ui.show_error("Application stopped by user.")
        return 130
    except Exception as error:
        ui.show_error(str(error))
        return 1


def console_main() -> int:
    return main()
