# JSONXGen

A tool to generate extraction code from JSON schemas. It supports multiple programming languages and provides both a command-line interface and a REST API.

## Installation

```bash
pip install jsonxgen
```

## Usage

### Command Line Interface

```bash
# Generate Python extraction code from a file (exact match)
jsonxgen --keywords name email --mode match data.json

# Generate Python extraction code from a JSON string (contains)
jsonxgen --keywords name --mode contains '{"user": {"name": "John"}}'

# Generate MySQL extraction code from a file (starts with)
jsonxgen --keywords name email --language mysql --mode startswith data.json

# Generate Spark SQL extraction code from a JSON string (exact match)
jsonxgen --keywords name --language "spark sql" '{"user": {"name": "John"}}'
```

### REST API

Start the server:
```bash
uvicorn src.server:app --reload
```

The API will be available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Example API request:
```bash
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{
           "json_input": "{\"user\": {\"name\": \"John\"}}",
           "keywords": ["name"],
           "mode": "match",
           "language": "python"
         }'
```

## Supported Languages

- Python
- MySQL
- Spark SQL
- PHP
- PySpark

## Features

- Multiple programming language support
- Different matching modes:
  - `match`: Exact match
  - `contains`: Substring match
  - `startswith`: Prefix match
- Command-line interface
- REST API with Swagger documentation
- Support for both file and JSON string input

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