import argparse
from .generator import create_project


def create_command(args):
    # maybe try to saperate the function
    if args.build_tool:
        create_project(name=args.name, build_tool=args.build_tool)
    else:
        create_project(name=args.name, template=args.template)


""" CForge """
parser = argparse.ArgumentParser(
    prog="cforge",
    description="Create clean C projects in seconds.",
    usage="cforge.exe <COMMAND> [OPTION] {VALUE}",
)

group = parser.add_mutually_exclusive_group()

""" Arguments """
parser.add_argument("name", help="Initialize a new project")
group.add_argument(
    "-b",
    "--build-tool",
    choices=["build.ninja", "Makefile"],
    help="Specify Build-Tool",
)
group.add_argument("-t", "--template", choices=["raylib", ""], help="Use a template")

parser.set_defaults(func=create_command)

""" Commands """
subparser = parser.add_subparsers(dest="command")

""" Adding Sub-Command """
# lib = subparser.add_parser("lib")
# lib.add_argument("-l", "--lib-name", action="store", help="Add custom library")

# package = subparser.add_parser("add")
# package.add_argument("-p", "--package", action="store", help="Install & add package manually")


def cforge_main():
    args = parser.parse_args()

    # jalankan semua function
    args.func(args)
