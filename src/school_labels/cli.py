"""Command-line interface for school-labels."""

import argparse
import csv
import sys

from . import generator


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate printable PDF labels from CSV data", prog="school-labels"
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


def main(argv: list[str] | None = None) -> int:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)

    # Read CSV data
    try:
        if args.input:
            with open(args.input, "r", newline="") as f:
                data = generator.read_csv_data(f)
        else:
            data = generator.read_csv_data(sys.stdin)
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
        return 1
    except (csv.Error, OSError) as e:
        print(f"Error reading CSV data: {e}", file=sys.stderr)
        return 1

    if not data:
        print("Error: No data found in input", file=sys.stderr)
        return 1

    # Determine template
    template = None
    if args.style:
        template = generator.TEMPLATES.get(args.style)
        if not template:
            print(f"Error: Unknown template style '{args.style}'", file=sys.stderr)
            return 1
    else:
        # Auto-detect template
        columns = list(data[0].keys())
        template = generator.detect_template(columns)
        if not template:
            print(
                f"Error: Could not auto-detect template from columns: {columns}",
                file=sys.stderr,
            )
            print("Available templates:", file=sys.stderr)
            for name, tmpl in generator.TEMPLATES.items():
                print(f"  {name}: requires {tmpl.required_columns}", file=sys.stderr)
            return 1

    # Validate columns
    missing = generator.validate_columns(data, template)
    if missing:
        print(
            f"Error: CSV is missing required columns: {', '.join(missing)}",
            file=sys.stderr,
        )
        return 1

    # Generate PDF
    try:
        pdf = generator.generate_labels(data, template, args.break_column)
    except (ValueError, OSError) as e:
        print(f"Error generating labels: {e}", file=sys.stderr)
        return 1

    # Output PDF
    try:
        if args.output == "-":
            # Output to stdout
            sys.stdout.buffer.write(pdf.output())
        else:
            # Output to file with conflict resolution
            output_filename = generator.generate_filename(args.output)
            pdf.output(output_filename)
            if output_filename != args.output:
                print(
                    f"Output written to {output_filename} (original filename existed)",
                    file=sys.stderr,
                )
    except OSError as e:
        print(f"Error writing output: {e}", file=sys.stderr)
        return 1

    return 0


def cli():
    """Console script entry point."""
    sys.exit(main())


if __name__ == "__main__":
    cli()
