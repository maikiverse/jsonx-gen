"""
Core functionality for JSON extraction code generation.
"""

import json
import os
from typing import Any, Dict, List, Union, Callable, Optional

def get_matcher(mode: str) -> Callable[[str, str], bool]:
    """
    Get the appropriate matching function based on the mode.
    
    Args:
        mode (str): One of 'match', 'contains', 'startswith', or 'endswith'
        
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
    elif mode == 'endswith':
        return lambda x, y: x.lower().endswith(y.lower())
    else:
        raise ValueError(f"Unsupported mode: {mode}. Must be one of: match, contains, startswith, endswith") 


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

def extract_json_path(
    json_obj: Union[Dict, List], 
    keywords: List[str], 
    mode: str = 'match',
    type: str = 'all'
) -> Dict[str, List[List[Union[str, int]]]]:
    """
    Extract paths from a JSON object that match the given keywords.
    
    Args:
        json_obj (Union[Dict, List]): The JSON object to analyze
        keywords (List[str]): List of keywords to search for in keys and values
        mode (str): Matching mode ('match', 'contains', 'startswith', or 'endswith')
        type (str): What to match ('all', 'key', or 'value')
        
    Returns:
        Dict[str, List[List[Union[str, int]]]]: Dictionary mapping keywords (with extensions for multiple matches) to their paths in the JSON structure
    """
    matches: Dict[str, List[List[Union[str, int]]]] = {}
    keyword_counts: Dict[str, int] = {k: 0 for k in keywords}
    matcher = get_matcher(mode)

    def get_key_with_extension(keyword: str) -> str:
        """Get the keyword with appropriate extension based on occurrence count."""
        count = keyword_counts[keyword]
        keyword_counts[keyword] += 1
        return f"{keyword}_{count}" if count > 0 else keyword

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
                    if type in ['all', 'key'] and matcher(str(k), keyword):
                        key = get_key_with_extension(keyword)
                        matches.setdefault(key, []).append(path + [k])
                    # Check if keyword matches the value (for primitive types)
                    if type in ['all', 'value'] and isinstance(v, (str, int, float)) and matcher(str(v), keyword):
                        key = get_key_with_extension(keyword)
                        matches.setdefault(key, []).append(path + [k])
                search(v, path + [k])
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                search(item, path + [idx])

    # Start the search from the root
    search(json_obj, [])
    return matches

def generate_extraction_code(
    json_input: Union[str, Dict, List],
    keywords: List[str],
    mode: str = 'match',
    type: str = 'all',
    target_language: Optional[str] = None
) -> str:
    """
    Generate code to extract fields from JSON based on keywords.
    
    Args:
        json_input: Either a JSON string, file path, or parsed JSON object
        keywords: List of keywords to search for
        mode: Matching mode ('match', 'contains', 'startswith', or 'endswith')
        type: What to match ('all', 'key', or 'value')
        target_language: Target language for the code (None for Python)
        
    Returns:
        str: Generated extraction code in the target language
        
    Raises:
        ValueError: If any of the input parameters are invalid
    """
    # Validate input parameters
    if not isinstance(keywords, list) or not keywords:
        raise ValueError("keywords must be a non-empty list")
    
    if not all(isinstance(k, str) for k in keywords):
        raise ValueError("all keywords must be strings")
    
    if mode not in ['match', 'contains', 'startswith', 'endswith']:
        raise ValueError(f"Invalid mode: {mode}. Must be one of: match, contains, startswith, endswith")
    
    if type not in ['all', 'key', 'value']:
        raise ValueError(f"Invalid type: {type}. Must be one of: all, key, value")
    
    # Parse JSON if it's a string
    if isinstance(json_input, str):
        try:
            json_obj = parse_json_input(json_input)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON input: {str(e)}")
    else:
        json_obj = json_input
    
    # Extract paths
    matches = extract_json_path(json_obj, keywords, mode, type)
    
    if not matches:
        return "# No matches found for the given keywords"
    
    # Get the appropriate generator and generate code
    from .code_generator_registry import CodeGeneratorRegistry
    language = target_language or 'python'
    try:
        generator = CodeGeneratorRegistry.get_generator(language)
        return generator(matches)
    except ValueError as e:
        raise ValueError(f"Error generating code: {str(e)}") 