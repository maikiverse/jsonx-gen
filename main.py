#!/usr/bin/env python3
"""
JSON Extraction Code Generator

This script provides a command-line tool that generates code to extract specific fields from JSON documents
based on keywords. It can generate extraction code in Python by default, and can also translate the code
to other languages like MySQL or Spark SQL using OpenAI's API.

The tool works by:
1. Parsing the input JSON (from file or string)
2. Searching for keywords in both keys and values using the specified matching mode
3. Generating extraction code in Python
4. Optionally translating the code to other languages using OpenAI's API.
"""

import argparse
import json
import os
from typing import Any, Dict, List, Union, Callable, Optional
import openai
from dotenv import load_dotenv

def get_matcher(mode: str) -> Callable[[str, str], bool]:
    """
    Get the appropriate matching function based on the mode.
    
    Args:
        mode (str): One of 'match', 'contains', or 'startswith'
        
    Returns:
        Callable[[str, str], bool]: A function that takes two strings and returns True if they match
        
    Raises:
        ValueError: If mode is not one of the supported values
    """
    mode = mode.lower()
    if mode == 'match':
        return lambda x, y: x.lower() == y.lower()
    elif mode == 'contains':
        return lambda x, y: y.lower() in x.lower()
    elif mode == 'startswith':
        return lambda x, y: x.lower().startswith(y.lower())
    else:
        raise ValueError(f"Unsupported mode: {mode}. Must be one of: match, contains, startswith")

def parse_json_input(json_input: str) -> Union[Dict, List]:
    """
    Parse JSON input from either a file path or a JSON string.
    
    Args:
        json_input (str): Either a path to a JSON file or a JSON string
        
    Returns:
        Union[Dict, List]: Parsed JSON object
        
    Raises:
        FileNotFoundError: If the input is a file path and the file doesn't exist
        json.JSONDecodeError: If the input is invalid JSON
    """
    # Check if the input looks like a file path
    if os.path.isfile(json_input):
        with open(json_input, 'r') as f:
            return json.load(f)
    
    # Try to parse as JSON string
    try:
        return json.loads(json_input)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON string: {str(e)}. If you meant to provide a file path, make sure the file exists.",
            e.doc,
            e.pos
        )

def generate_python_extraction_code(json_obj: Union[Dict, List], keywords: List[str], mode: str = 'match') -> str:
    """
    Generate Python code to extract fields from a JSON object based on keywords.
    
    Args:
        json_obj (Union[Dict, List]): The JSON object to analyze
        keywords (List[str]): List of keywords to search for in keys and values
        mode (str): Matching mode ('match', 'contains', or 'startswith')
        
    Returns:
        str: Python code that extracts matching fields from the JSON object
        
    Example:
        >>> json_obj = {"user": {"name": "John", "email": "john@example.com"}}
        >>> keywords = ["name", "email"]
        >>> print(generate_python_extraction_code(json_obj, keywords))
        result_doc = {
            "name": doc["user"]["name"],
            "email": doc["user"]["email"],
        }
    """
    matches: Dict[str, List[str]] = {}
    matcher = get_matcher(mode)

    def path_to_str(path: List[Union[str, int]]) -> str:
        """Convert a path list to a string representation for Python code."""
        return "".join(f"[{json.dumps(p)}]" for p in path)

    def search(obj: Any, path: List[Union[str, int]]) -> None:
        """
        Recursively search through the JSON object for keywords.
        
        Args:
            obj: Current object being searched
            path: Current path in the JSON structure
        """
        if isinstance(obj, dict):
            for k, v in obj.items():
                for keyword in keywords:
                    # Check if keyword matches the key
                    if matcher(str(k), keyword):
                        matches.setdefault(keyword, []).append(path_to_str(path + [k]))
                    # Check if keyword matches the value (for primitive types)
                    if isinstance(v, (str, int, float)) and matcher(str(v), keyword):
                        matches.setdefault(keyword, []).append(path_to_str(path + [k]))
                search(v, path + [k])
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                search(item, path + [idx])

    # Start the search from the root
    search(json_obj, [])

    # Generate the extraction code
    lines = ["result_doc = {"]
    for keyword, paths in matches.items():
        for i, path in enumerate(paths):
            label = f"{keyword}_{i}" if i > 0 else keyword
            lines.append(f"    \"{label}\": doc{path},")
    lines.append("}")
    return "\n".join(lines)

def translate_to_language(python_code: str, target_language: str) -> str:
    """
    Translate Python extraction code to another programming language using OpenAI API.
    
    Args:
        python_code (str): The Python code to translate
        target_language (str): The target programming language
        
    Returns:
        str: The translated code in the target language
        
    Raises:
        ValueError: If OpenAI API key is not found in environment variables
    """
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    client = openai.OpenAI(api_key=api_key)
    
    prompt = f"""Translate the following Python code to {target_language}. 
    The code extracts specific fields from a JSON document based on keywords.
    Here's the Python code:
    
    {python_code}
    
    Please provide only the translated code without any explanations."""
    
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You are a code translation expert."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return response.choices[0].message.content

def generate_extraction_code(
    json_input: Union[str, Dict, List],
    keywords: List[str],
    mode: str = 'match',
    target_language: Optional[str] = None
) -> str:
    """
    Generate code to extract fields from JSON based on keywords.
    
    Args:
        json_input: Either a JSON string, file path, or parsed JSON object
        keywords: List of keywords to search for
        mode: Matching mode ('match', 'contains', or 'startswith')
        target_language: Target language for the code (None for Python)
        
    Returns:
        str: Generated extraction code in the target language
        
    Example:
        >>> json_str = '{"user": {"name": "John"}}'
        >>> code = generate_extraction_code(json_str, ["name"])
        >>> print(code)
        result_doc = {
            "name": doc["user"]["name"],
        }
        
        >>> # Generate MySQL code
        >>> mysql_code = generate_extraction_code(json_str, ["name"], target_language="mysql")
    """
    # Parse JSON if it's a string
    if isinstance(json_input, str):
        json_obj = parse_json_input(json_input)
    else:
        json_obj = json_input
    
    # Generate Python code
    python_code = generate_python_extraction_code(json_obj, keywords, mode)
    
    # Return Python code or translate to target language
    if target_language is None or target_language.lower() == 'python':
        return python_code
    else:
        return translate_to_language(python_code, target_language)

def main():
    """Main entry point for the command-line interface."""
    parser = argparse.ArgumentParser(
        description='Generate extraction code from JSON schema',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Generate Python extraction code from a file (exact match):
    python main.py --keywords name email --mode match data.json

  Generate Python extraction code from a JSON string (contains):
    python main.py --keywords name --mode contains '{"user": {"name": "John"}}'

  Generate MySQL extraction code from a file (starts with):
    python main.py --keywords name email --language mysql --mode startswith data.json

  Generate Spark SQL extraction code from a JSON string (exact match):
    python main.py --keywords name --language "spark sql" '{"user": {"name": "John"}}'
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
        choices=['match', 'contains', 'startswith'],
        default='match',
        help='Matching mode: match (exact), contains (substring), or startswith (prefix)'
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
        print(f"Error: File '{args.json_input}' not found")
        exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: {str(e)}")
        exit(1)
    except ValueError as e:
        print(f"Error: {str(e)}")
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main() 