# school-labels

CLI tool that generates printable PDF labels from CSV data, laid out for Avery 7160 label sheets (3x7 grid, A4).

## Installation

Requires Python 3.13+.

```bash
pip install school-labels
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add school-labels
```

## Usage

```bash
# Auto-detect template from CSV columns
school-labels students.csv

# Explicit template
school-labels --style email-password students.csv

# Page break when a column value changes (pre-sort by this column)
school-labels --break group students.csv

# Custom output path (default: labels.pdf)
school-labels -o output.pdf students.csv

# Read from stdin, write to stdout
cat students.csv | school-labels --output -
```

## Templates

### email-password

Generates labels showing student email and password credentials.

Required CSV columns: `admin`, `last_name`, `first_name`, `group`, `email`, `password`


## Python API

```python
from pathlib import Path
from school_labels import generate_labels

data = [
    {
        "admin": "1001",
        "first_name": "John",
        "last_name": "Smith",
        "group": "7A",
        "email": "john.smith@school.org",
        "password": "Pass1234",
    },
]

pdf_bytes = generate_labels(data, "email-password")
Path("labels.pdf").write_bytes(pdf_bytes)
```

Pass `break_column` to insert a page break when a column's value changes (pre-sort your data by that column):

```python
pdf_bytes = generate_labels(data, "email-password", break_column="group")
```

For direct access to the underlying `FPDF` object (e.g. to merge pages or set metadata), use the template's `create_pdf` method:

```python
from school_labels import TEMPLATES

fpdf = TEMPLATES["email-password"].create_pdf(data)
```

## Development

```bash
uv sync       # Install dependencies
just check    # Lint + test
just test     # Test only
just lint     # Lint only
just format   # Format code
```
