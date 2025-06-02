# JSONx-Gen

A tool to search JSON objects/files for keywords and generate extraction code for all matching paths. It supports multiple programming languages and provides both a command-line interface and a web-based GUI.

## Features

- Search JSON for keywords in keys and/or values
- Multiple matching modes:
  - `match`: Exact match
  - `contains`: Substring match
  - `startswith`: Prefix match
  - `endswith`: Suffix match
- Multiple match types:
  - `all`: Match both keys and values
  - `key`: Match only keys
  - `value`: Match only values
- Support for various input sources:
  - Local JSON files
  - URLs pointing to JSON data
  - JSON strings
  - JSON objects (in API requests)
- Web-based GUI for easy interaction
- Command-line interface for automation
- REST API for integration

## Installation

```bash
pip install jsonx_gen
```

## Usage

### Web Interface

Start the server:
```bash
uvicorn jsonx_gen.server:app --reload
```

Then open your browser at http://localhost:8000 to use the web interface.

### Command Line Interface

```bash
# Generate Python extraction code from a local file (exact match)
jsonx_gen --keywords "name,email" --mode match data.json

# Generate Python extraction code from a URL (contains)
jsonx_gen --keywords "name" --mode contains "https://api.example.com/data.json"

# Generate Python extraction code from a JSON string (contains)
jsonx_gen --keywords "name" --mode contains '{"user": {"name": "John"}}'

# Generate MySQL extraction code from a URL (starts with)
jsonx_gen --keywords "name,email" --language mysql --mode startswith "https://api.example.com/data.json"

# Generate Spark SQL extraction code from a JSON string (exact match)
jsonx_gen --keywords "name" --language "spark_sql" '{"user": {"name": "John"}}'

# Generate code matching only keys (endswith)
jsonx_gen --keywords "id" --mode endswith --type key data.json
```

### REST API

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
