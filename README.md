# school-labels

CLI tool that generates printable PDF labels from CSV data, laid out for Avery 7160 label sheets (3x7 grid, A4).

## Installation

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Usage

```bash
# Auto-detect template from CSV columns
uv run school-labels students.csv

# Explicit template
uv run school-labels --style email-password students.csv

# Page break when a column value changes (pre-sort by this column)
uv run school-labels --break group students.csv

# Custom output path (default: labels.pdf)
uv run school-labels -o output.pdf students.csv

# Read from stdin, write to stdout
cat students.csv | uv run school-labels --output -
```

## Templates

### email-password

Generates labels showing student email and password credentials.

Required CSV columns: `admin`, `last_name`, `first_name`, `group`, `email`, `password`


## Development

```bash
just check    # Lint + test
just test     # Test only
just lint     # Lint only
just format   # Format code
```
