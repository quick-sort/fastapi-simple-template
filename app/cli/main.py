import argparse
import asyncio
import sys


def main():
    parser = argparse.ArgumentParser(description="CLI for app commands")
    subparsers = parser.add_subparsers(dest="command")
    from app.cli.init_user import registry_command

    registry_command(subparsers)

    from app.cli.echo import registry_command

    registry_command(subparsers)

    args = parser.parse_args(sys.argv[1:])
    if hasattr(args, "func"):
        if asyncio.iscoroutinefunction(args.func):
            asyncio.run(args.func(args))
        else:
            args.func(args)
    else:
        parser.print_help()
