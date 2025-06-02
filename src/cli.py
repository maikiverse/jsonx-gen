"""
Command-line interface for JSON extraction code generation.
"""

import argparse
import sys
from .core import generate_extraction_code

def main():
    """Main entry point for the command-line interface."""
    parser = argparse.ArgumentParser(
        description='Generate extraction code from JSON schema',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Generate Python extraction code from a file (exact match):
    jsonxgen --keywords "name,email" --mode match data.json

  Generate JavaScript extraction code from a JSON string (contains):
    jsonxgen --keywords "name" --mode contains --language javascript '{"user": {"name": "John"}}'

  Generate MongoDB extraction code from a file (match):
    jsonxgen --keywords "name,email" --language mongodb --mode match data.json

  Generate MySQL extraction code from a file (starts with):
    jsonxgen --keywords "name,email" --language mysql --mode startswith data.json

  Generate Spark SQL extraction code from a JSON string (exact match):
    jsonxgen --keywords "name" --language "spark_sql" '{"user": {"name": "John"}}'


    
    parser.add_argument(
        '--keywords',
        required=True,
        help='Comma-separated list of keywords to search for in the JSON'
    )
    parser.add_argument(
        '--mode',
        choices=['match', 'contains', 'startswith', 'endswith'],
        default='match',
        help='Matching mode: match (exact), contains (substring), startswith (prefix), or endswith (suffix)'
    )
    parser.add_argument(
        '--type',
        choices=['all', 'key', 'value'],
        default='all',
        help='What to match: all (both keys and values), key (only keys), or value (only values)'
    )
    parser.add_argument(
        '--language',
        default='python',
        help='Target language for the extraction code. Supported languages: c#, c++, go, java, javascript, matlab, mongodb, mysql, php, postgresql, python, pyspark, r, ruby, rust, shell, spark_sql'
    )
    parser.add_argument(
        'json_input',
        help='Path to a JSON file or a JSON string to analyze (must be the last argument)'
    )
    
    args = parser.parse_args()
    
    try:
        # Split keywords by comma and strip whitespace
        keywords = [k.strip() for k in args.keywords.split(',')]
        
        code = generate_extraction_code(
            args.json_input,
            keywords,
            args.mode,
            args.type,
            args.language
        )
        print(code)
            
    except FileNotFoundError:
        print(f"Error: File '{args.json_input}' not found", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 