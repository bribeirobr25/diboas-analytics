"""
Registry command - list available implementations.

Provides visibility into the pluggable registry framework.
"""

import logging

logger = logging.getLogger(__name__)


def run_registry(args):
    """
    List available registry implementations.

    Args:
        args: Parsed command line arguments with --type option
    """
    from src.registries import list_all_registrations, ensure_collectors_registered

    # Ensure all collectors are registered before listing
    ensure_collectors_registered()

    print("Registry Framework - Available Implementations")
    print("=" * 55)
    print()

    all_regs = list_all_registrations()

    registry_type = getattr(args, 'type', 'all')

    if registry_type == 'all':
        registries_to_show = all_regs.keys()
    else:
        registries_to_show = [registry_type]

    for reg_name in registries_to_show:
        if reg_name not in all_regs:
            continue

        implementations = all_regs[reg_name]
        print(f"{reg_name.upper()}")
        print("-" * 40)

        if implementations:
            for impl in sorted(implementations):
                # Mark stubs
                stub_marker = ""
                if reg_name == 'triggers' or (reg_name == 'personas'):
                    stub_marker = " (stub)"
                elif reg_name == 'outputs' and impl in ['newsletter_md', 'twitter_thread', 'website_teaser']:
                    stub_marker = " (stub)"

                print(f"  - {impl}{stub_marker}")
        else:
            print("  (none registered)")

        print()

    # Print usage examples
    print("Usage Examples:")
    print("-" * 40)
    print()
    print("  # Get engine through registry")
    print("  from src.registries import EngineRegistry")
    print("  engine = EngineRegistry.get_instance().get('battle_test', {})")
    print("  results = engine.run(data=None, config={'scenario': 'A'})")
    print()
    print("  # Get collector through registry")
    print("  from src.registries import CollectorRegistry")
    print("  collector = CollectorRegistry.get_instance().get('file_loader', {})")
    print("  data = collector.collect()")
    print()
    print("  # Get validator through registry")
    print("  from src.registries import ValidatorRegistry")
    print("  validator = ValidatorRegistry.get_instance().get('result_validator', {})")
    print("  result = validator.validate_cv01([100, 150, 200])")
    print()
