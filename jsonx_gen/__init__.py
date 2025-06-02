"""
JSONXGen - JSON Extraction Code Generator

A tool that generates code to extract specific fields from JSON documents based on keywords.
Supports multiple output languages and provides both CLI and REST API interfaces.
"""

from .core import extract_json_path, generate_extraction_code

__all__ = ['extract_json_path', 'generate_extraction_code']

__version__ = "0.1.0" 