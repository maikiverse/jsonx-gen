"""
Utility functions for JSON extraction code generation.
"""

import json
import os
import requests
from typing import Any, Dict, List, Union, Callable
from urllib.parse import urlparse

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

def is_valid_url(url: str) -> bool:
    """
    Check if a string is a valid URL.
    
    Args:
        url (str): The URL to validate
        
    Returns:
        bool: True if the URL is valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def parse_json_input(json_input: Union[str, Dict, List]) -> Union[Dict, List]:
    """
    Parse JSON input from either a file path, URL, a JSON string, or return an already parsed JSON object.
    
    Args:
        json_input (Union[str, Dict, List]): Either a path to a JSON file, a URL, a JSON string, or an already parsed JSON object
        
    Returns:
        Union[Dict, List]: Parsed JSON object
        
    Raises:
        FileNotFoundError: If the input is a file path and the file doesn't exist
        json.JSONDecodeError: If the input is invalid JSON
        requests.RequestException: If there's an error fetching from URL
        ValueError: If the input is neither a valid file path, URL, nor JSON string
    """
    # If input is already a Dict or List, return it directly
    if isinstance(json_input, (dict, list)):
        return json_input
        
    # Check if the input is a URL
    if is_valid_url(json_input):
        try:
            response = requests.get(json_input)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()
        except requests.RequestException as e:
            raise ValueError(f"Error fetching JSON from URL: {str(e)}")
    
    # Check if the input is a file path
    if os.path.isfile(json_input):
        with open(json_input, 'r') as f:
            return json.load(f)
    
    # Try to parse as JSON string
    try:
        return json.loads(json_input)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON string: {str(e)}. If you meant to provide a file path or URL, make sure it exists and is accessible.",
            e.doc,
            e.pos
        )

def validate_extraction_params(keywords: List[str], mode: str, type: str) -> None:
    """
    Validate the parameters for JSON extraction.
    
    Args:
        keywords (List[str]): List of keywords to search for
        mode (str): Matching mode
        type (str): What to match
        
    Raises:
        ValueError: If any of the parameters are invalid
    """
    if not isinstance(keywords, list) or not keywords:
        raise ValueError("keywords must be a non-empty list")
    
    if not all(isinstance(k, str) for k in keywords):
        raise ValueError("all keywords must be strings")
    
    if mode not in ['match', 'contains', 'startswith', 'endswith']:
        raise ValueError(f"Invalid mode: {mode}. Must be one of: match, contains, startswith, endswith")
    
    if type not in ['all', 'key', 'value']:
        raise ValueError(f"Invalid type: {type}. Must be one of: all, key, value")

def get_key_with_extension(keyword: str, keyword_counts: Dict[str, int]) -> str:
    """
    Get the keyword with appropriate extension based on occurrence count.
    
    Args:
        keyword (str): The keyword to process
        keyword_counts (Dict[str, int]): Dictionary tracking keyword occurrences
        
    Returns:
        str: The keyword with appropriate extension
    """
    count = keyword_counts[keyword]
    keyword_counts[keyword] += 1
    return f"{keyword}_{count}" if count > 0 else keyword 