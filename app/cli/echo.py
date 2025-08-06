import argparse


async def command(args):
    print(args)


def registry_command(parser: argparse.ArgumentParser):
    echo_parser = parser.add_parser("echo", help="Echo command")
    echo_parser.set_defaults(func=command)
    echo_parser.add_argument("--name", help="Name")
    return echo_parser
