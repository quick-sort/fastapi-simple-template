import argparse
import asyncio
import importlib.util
import os
import sys


def import_sub_commands(subparsers):
    """
    Lists all Python (.py) files in the same directory as the current script.
    For each file, attempts to import it as a module and call its 'registry'
    function if defined.
    """
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Iterate over all files in the directory
    for filename in os.listdir(current_dir):
        if filename.endswith(".py") and filename != os.path.basename(__file__):
            filepath = os.path.join(current_dir, filename)

            # Derive module name (without .py extension)
            module_name = os.path.splitext(filename)[0]

            # Avoid re-importing if already loaded (optional, but good practice)
            if module_name in sys.modules:
                module = sys.modules[module_name]
            else:
                # Load the module from file
                spec = importlib.util.spec_from_file_location(module_name, filepath)
                if spec is None:
                    continue
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module  # Cache the module
                try:
                    spec.loader.exec_module(module)
                except Exception as e:
                    print(f"Failed to import {filename}: {e}")
                    continue

            # Check if 'registry' function exists in the module
            if hasattr(module, "registry_command") and callable(
                module.registry_command
            ):
                try:
                    module.registry_command(subparsers)
                except Exception as e:
                    print(f"Error calling registry() in {filename}: {e}")


def main():
    parser = argparse.ArgumentParser(description="CLI for app commands")
    subparsers = parser.add_subparsers(dest="command")
    import_sub_commands(subparsers)
    args = parser.parse_args(sys.argv[1:])
    if hasattr(args, "func"):
        if asyncio.iscoroutinefunction(args.func):
            asyncio.run(args.func(args))
        else:
            args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
