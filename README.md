# JSONx-Gen

A tool to search a JSON object for keywords and generate extraction code to all matching paths.
It supports multiple programming languages and provides both a command-line interface and a web-based GUI.

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

### Basic Installation (CLI only)
```bash
pip install jsonx_gen
```

### With Web Interface
```bash
pip install jsonx_gen[web]
```


## Usage

### Python Package Usage

```python
from jsonx_gen import extract_json_path, generate_extraction_code

# Example JSON data
json_data = {
    "user": {
        "name": "John Doe",
        "email": "john@example.com",
        "address": {
            "street": "123 Main St",
            "city": "Boston"
        }
    }
}

# Extract paths for matching keywords and values
paths = extract_json_path(
    json_data,
    keywords=["name", "email"],
    mode="match",  # Options: match, contains, startswith, endswith
    type="all"     # Options: all, key, value
)

# Generate extraction code in JavaScript with URL input
code = generate_extraction_code(
    "https://api.example.com/data.json",
    language="javascript",
    mode="match",
    type="all"
)
print(code)
```

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

# Generate Spark SQL extraction code from a URL (contains)
jsonx_gen --keywords "name" --language "spark_sql" --mode contains "https://api.example.com/data.json"

# Generate Java extraction code from a JSON string (startswith)
jsonx_gen --keywords "name" --language "java" --mode startswith '{"user": {"name": "John"}}'
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
   pip install -e ".[web]"
   ```

## License

MIT License
