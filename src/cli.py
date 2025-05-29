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
    jsonpathxgen --keywords name email --mode match data.json

  Generate Python extraction code from a JSON string (contains):
    jsonpathxgen --keywords name --mode contains '{"user": {"name": "John"}}'

  Generate MySQL extraction code from a file (starts with):
    jsonpathxgen --keywords name email --language mysql --mode startswith data.json

  Generate Spark SQL extraction code from a JSON string (exact match):
    jsonpathxgen --keywords name --language "spark sql" '{"user": {"name": "John"}}'
        """
    )
    
    parser.add_argument(
        '--keywords',
        nargs='+',
        required=True,
        help='Keywords to search for in the JSON'
    )
    parser.add_argument(
        '--mode',
        choices=['match', 'contains', 'startswith', 'endswith'],
        default='match',
        help='Matching mode: match (exact), contains (substring), startswith (prefix), or endswith (suffix)'
    )
    parser.add_argument(
        '--language',
        default='python',
        help='Target language for the extraction code (default: python)'
    )
    parser.add_argument(
        'json_input',
        help='Path to a JSON file or a JSON string to analyze (must be the last argument)'
    )
    
    args = parser.parse_args()
    
    try:
        code = generate_extraction_code(
            args.json_input,
            args.keywords,
            args.mode,
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