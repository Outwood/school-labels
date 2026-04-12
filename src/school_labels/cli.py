"""Command-line interface for school-labels."""

import argparse
import csv
import sys
from importlib.metadata import version
from pathlib import Path
from typing import Any

from . import generator
from .templates import LabelTemplate


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate printable PDF labels from CSV data", prog="school-labels"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {version('school-labels')}"
    )
    parser.add_argument("input", nargs="?", help="CSV input file (default: stdin)")
    parser.add_argument(
        "--style", choices=list(generator.TEMPLATES.keys()), help="Label template style"
    )
    parser.add_argument(
        "--output",
        "-o",
        default="labels.pdf",
        help='Output PDF file (use "-" for stdout, default: labels.pdf)',
    )
    parser.add_argument(
        "--break",
        dest="break_column",
        help="Column name to trigger page breaks on value changes",
    )

    return parser


def _load_csv_data(args: argparse.Namespace) -> list[dict[str, Any]] | None:
    """Read CSV data from file or stdin, returning None on error."""
    try:
        if args.input:
            with Path(args.input).open(newline="") as f:
                data = generator.read_csv_data(f)
        else:
            data = generator.read_csv_data(sys.stdin)
    except FileNotFoundError:
        sys.stderr.write(f"Error: Input file '{args.input}' not found\n")
        return None
    except (csv.Error, OSError) as e:
        sys.stderr.write(f"Error reading CSV data: {e}\n")
        return None
    if not data:
        sys.stderr.write("Error: No data found in input\n")
        return None
    return data


def _resolve_template(
    args: argparse.Namespace, data: list[dict[str, Any]]
) -> LabelTemplate | None:
    """Determine template from args or auto-detect, returning None on error."""
    if args.style:
        template = generator.TEMPLATES.get(args.style)
        if not template:
            sys.stderr.write(f"Error: Unknown template style '{args.style}'\n")
            return None
        return template
    columns = list(data[0].keys())
    template = generator.detect_template(columns)
    if not template:
        sys.stderr.write(
            f"Error: Could not auto-detect template from columns: {columns}\n"
        )
        sys.stderr.write("Available templates:\n")
        for name, tmpl in generator.TEMPLATES.items():
            sys.stderr.write(f"  {name}: requires {tmpl.required_columns}\n")
        return None
    return template


def main(argv: list[str] | None = None) -> int:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)

    data = _load_csv_data(args)
    if data is None:
        return 1

    template = _resolve_template(args, data)
    if template is None:
        return 1

    missing = generator.validate_columns(data, template)
    if missing:
        sys.stderr.write(
            f"Error: CSV is missing required columns: {', '.join(missing)}\n"
        )
        return 1

    try:
        pdf_bytes = generator.generate_labels(
            data, template.name, break_column=args.break_column
        )
    except (ValueError, OSError) as e:
        sys.stderr.write(f"Error generating labels: {e}\n")
        return 1

    try:
        if args.output == "-":
            sys.stdout.buffer.write(pdf_bytes)
        else:
            output_filename = generator.generate_filename(args.output)
            Path(output_filename).write_bytes(pdf_bytes)
            if output_filename != args.output:
                sys.stderr.write(
                    f"Output written to {output_filename} (original filename existed)\n"
                )
    except OSError as e:
        sys.stderr.write(f"Error writing output: {e}\n")
        return 1

    return 0


def cli() -> None:
    """Console script entry point."""
    sys.exit(main())


if __name__ == "__main__":
    cli()
