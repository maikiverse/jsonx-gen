"""
Core functionality for JSON extraction code generation.
"""

import json
import os
import json_stream
from typing import Any, Dict, List, Union, Optional
from .utils import (
    get_matcher,
    is_valid_url,
    parse_json_input,
    validate_extraction_params,
    get_key_with_extension
)
from .code_generator_registry import CodeGeneratorRegistry

# Define threshold for large files (10MB)
LARGE_FILE_THRESHOLD = 10 * 1024 * 1024  # 10MB in bytes
# LARGE_FILE_THRESHOLD = 10


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
        Dict[str, List[List[Union[str, int]]]]: Dictionary mapping keywords to their paths
    """
    keywords = list(set(keywords))
    matches: Dict[str, List[List[Union[str, int]]]] = {}
    keyword_counts: Dict[str, int] = {k: 0 for k in keywords}
    matcher = get_matcher(mode)

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
                        key = get_key_with_extension(keyword, keyword_counts)
                        matches.setdefault(key, []).append(path + [k])
                    # Check if keyword matches the value (for primitive types)
                    if type in ['all', 'value'] and isinstance(v, (str, int, float)) and matcher(str(v), keyword):
                        key = get_key_with_extension(keyword, keyword_counts)
                        matches.setdefault(key, []).append(path + [k])
                search(v, path + [k])
        elif isinstance(obj, list):
            for idx, item in enumerate(obj):
                # match value and item is atomic
                if type in ['all', 'value'] and isinstance(item, (str, int, float)):
                    for keyword in keywords:
                        if matcher(str(item), keyword):
                            key = get_key_with_extension(keyword, keyword_counts)
                            matches.setdefault(key, []).append(path + [idx])
                else:
                    # item is dict or list
                    search(item, path + [idx])

    # Start the search from the root
    search(json_obj, [])
    return dict(sorted(matches.items()))


def extract_json_path_streaming(
    file_path: str,
    keywords: List[str],
    mode: str = 'match',
    type: str = 'all'
) -> Dict[str, List[List[Union[str, int]]]]:
    """
    Extract paths from a streaming JSON file that match the given keywords.

    Args:
        file_path (str): Path to the JSON file
        keywords (List[str]): List of keywords to search for in keys and/or values
        mode (str): Matching mode ('match', 'contains', 'startswith', or 'endswith')
        type (str): What to match ('all', 'key', or 'value')

    Returns:
        Dict[str, List[List[Union[str, int]]]]: Dictionary mapping keywords to their matched paths
    """
    keywords = list(set(keywords))
    matches: Dict[str, List[List[Union[str, int]]]] = {}
    keyword_counts: Dict[str, int] = {k: 0 for k in keywords}
    matcher = get_matcher(mode)
    prev_path: List[Union[str, int]] = []

    def visitor(item: Any, path: tuple):
        nonlocal prev_path
        path = list(path)

        # compute delta
        i = 0
        while i < len(path) and i < len(prev_path) and path[i] == prev_path[i]:
            i += 1
        delta = path[i:]
        base_path = path[:i]

        # only process unmatched suffix for keys
        if type in ['all', 'key']:
            for j, part in enumerate(delta):
                if isinstance(part, str):
                    for keyword in keywords:
                        if matcher(part, keyword):
                            key = get_key_with_extension(keyword, keyword_counts)
                            matches.setdefault(key, []).append(base_path + delta[:j+1])
                            # break
                    else:
                        # jump to next part
                        continue
                    break

        # check value
        if type in ['all', 'value'] and isinstance(item, (str, int, float)):
            for keyword in keywords:
                if matcher(str(item), keyword):
                    key = get_key_with_extension(keyword, keyword_counts)
                    matches.setdefault(key, []).append(path)
                    break

        prev_path = path

    with open(file_path, 'r') as f:
        json_stream.visit(f, visitor)

    return dict(sorted(matches.items()))


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
    validate_extraction_params(keywords, mode, type)

    use_streaming = (
        isinstance(json_input, str)
        and os.path.isfile(json_input)
        and os.path.getsize(json_input) > LARGE_FILE_THRESHOLD
        )

    if use_streaming:
        matches = extract_json_path_streaming(json_input, keywords, mode, type)
    else:
        try:
            json_obj = parse_json_input(json_input)
            matches = extract_json_path(json_obj, keywords, mode, type)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON input: {str(e)}")
            
    if not matches:
        return "# No matches found for the given keywords"
    
    # Get the appropriate generator and generate code
    language = target_language or 'python'
    try:
        generator = CodeGeneratorRegistry.get_generator(language)
        return generator(matches)
    except ValueError as e:
        raise ValueError(f"Error generating code: {str(e)}") 