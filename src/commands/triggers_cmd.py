"""
Triggers command handler - Evaluate intelligence triggers.
"""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def run_triggers(args):
    """
    Run intelligence trigger evaluation.

    Args:
        args: CLI arguments with:
            - data: Optional path to market data JSON
            - output: Output file path
            - dry_run: If True, don't record cooldowns
    """
    from src.triggers import IntelligenceTriggerEvaluator

    print("Evaluating intelligence triggers...")
    print()

    # Load data
    data = {}
    if args.data:
        data_path = Path(args.data)
        if data_path.exists():
            with open(data_path) as f:
                data = json.load(f)
            print(f"  Loaded data from: {args.data}")
        else:
            print(f"  Warning: Data file not found: {args.data}")
    else:
        print("  No data file specified, using empty data set")
        print("  (Triggers may not fire without live data)")

    # Create evaluator
    config = {
        "default_cooldown_minutes": 0 if args.dry_run else 60,
        "consolidate_alerts": True,
    }
    evaluator = IntelligenceTriggerEvaluator(config=config)

    # Evaluate all triggers
    results = evaluator.evaluate_all(data)

    # Count results
    fired = [r for r in results if r.fired]
    total = len(results)

    print()
    print(f"  Total triggers evaluated: {total}")
    print(f"  Triggers fired: {len(fired)}")
    print()

    # Show fired triggers
    if fired:
        print("  Fired triggers:")
        for r in fired:
            print(f"    [{r.priority.value}] {r.trigger_id}: {r.condition_description}")
            if r.affected_strategies:
                print(f"        Affects strategies: {r.affected_strategies}")
        print()

    # Save results
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_data = {
        "total_triggers": total,
        "fired_count": len(fired),
        "dry_run": args.dry_run,
        "results": [
            {
                "trigger_id": r.trigger_id,
                "fired": r.fired,
                "priority": r.priority.value,
                "category": r.category.value,
                "action": r.action.value,
                "affected_strategies": r.affected_strategies,
                "condition": r.condition_description,
                "threshold": r.threshold,
                "actual_value": r.actual_value,
            }
            for r in results
        ]
    }

    with open(output_path, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"  Results saved to: {output_path}")

    if args.dry_run:
        print()
        print("  (Dry run - cooldowns not recorded)")
