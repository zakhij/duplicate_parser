from pathlib import Path
import argparse
from duplicate_finder import DuplicateFinder


def parse_args() -> argparse.Namespace:
    """Parse command line arguments.
    Returns:
        argparse.Namespace: The parsed arguments, i.e. the input file path.
    """
    parser = argparse.ArgumentParser(
        description="Find potential duplicate company names in a text file."
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Path to input file containing company names",
        default=Path("data_files/input.txt"),
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point for the duplicate finder CLI."""
    args = parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f"Input file not found: {args.input}")

    finder = DuplicateFinder()
    finder.find_duplicates(args.input)


if __name__ == "__main__":
    main()
