# JSONXGen

A tool to generate extraction code from JSON schemas. It supports multiple programming languages and provides both a command-line interface and a REST API.

## Installation

```bash
pip install jsonxgen
```

## Usage

### Command Line Interface

```bash
# Generate Python extraction code from a local file (exact match)
jsonxgen --keywords "name,email" --mode match data.json

# Generate Python extraction code from a URL (contains)
jsonxgen --keywords "name" --mode contains "https://api.example.com/data.json"

# Generate Python extraction code from a JSON string (contains)
jsonxgen --keywords "name" --mode contains '{"user": {"name": "John"}}'

# Generate MySQL extraction code from a URL (starts with)
jsonxgen --keywords "name,email" --language mysql --mode startswith "https://api.example.com/data.json"

# Generate Spark SQL extraction code from a JSON string (exact match)
jsonxgen --keywords "name" --language "spark sql" '{"user": {"name": "John"}}'

# Generate code matching only keys (endswith)
jsonxgen --keywords "id" --mode endswith --type key data.json
```

### REST API

Start the server:
```bash
uvicorn src.server:app --reload
```

The API will be available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Example API requests:
```bash
# Using a local file
curl -X POST "http://localhost:8000/extract" \
     -H "Content-Type: application/json" \
     -d '{
           "json_obj": {"user": {"name": "John"}},
           "keywords": ["name"],
           "mode": "match",
           "type": "all",
           "language": "python"
         }'

# Using a URL
curl "http://localhost:8000/extract?file_path=https://api.example.com/data.json&keywords=name,email&mode=match&type=all"
```

## Supported Input Sources

- Local JSON files
- URLs pointing to JSON data
- JSON strings
- JSON objects (in API requests)

## Supported Languages

- C#
- C++
- Go
- Java
- JavaScript
- MATLAB
- MongoDB
- MySQL
- PHP
- PostgreSQL
- Python
- PySpark
- R
- Ruby
- Rust
- Shell
- Spark SQL

## Features

- Multiple programming language support
- Different matching modes:
  - `match`: Exact match
  - `contains`: Substring match
  - `startswith`: Prefix match
  - `endswith`: Suffix match
- Different match types:
  - `all`: Match both keys and values
  - `key`: Match only keys
  - `value`: Match only values
- Command-line interface
- REST API with Swagger documentation
- Support for multiple input sources (files, URLs, strings)

## Development

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Run tests:
   ```bash
   pytest
   ```

## License

MIT License