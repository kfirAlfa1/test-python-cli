import argparse

from greet_cli import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="greet", description="Greet someone from the terminal.")
    parser.add_argument("name", nargs="?", default="world", help="who to greet")
    parser.add_argument("-n", "--times", type=int, default=1, help="how many times to greet")
    parser.add_argument("--shout", action="store_true", help="greet in upper case")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    message = f"Hello, {args.name}!"
    if args.shout:
        message = message.upper()
    for _ in range(args.times):
        print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
