from typing import Dict, List, Union, Callable
import json

class CodeGeneratorRegistry:
    _generators = {}

    @classmethod
    def register(cls, language: str):
        def decorator(func):
            cls._generators[language] = func
            return func
        return decorator

    @classmethod
    def get_generator(cls, language: str) -> Callable[[Dict[str, List[List[Union[str, int]]]]], str]:
        if language not in cls._generators:
            supported_languages = sorted(cls._generators.keys())
            raise ValueError(f"'{language}' not in supported languages {supported_languages}")
        return cls._generators[language]

def path_to_str(path: List[Union[str, int]]) -> str:
    """Convert a path list to a string representation for Python code."""
    return "".join(f"[{json.dumps(p)}]" for p in path)

@CodeGeneratorRegistry.register('python')
def generate_extraction_code_python(matches: Dict[str, List[List[Union[str, int]]]]) -> str:
    """
    Generate Python code to extract fields from a JSON object based on extracted paths.
    
    Args:
        matches (Dict[str, List[List[Union[str, int]]]]): Dictionary mapping keywords to their paths
        
    Returns:
        str: Python code that extracts matching fields from the JSON object
    """
    lines = [
        "import json",
        "",
        "with open(\"<yourfilepath>.json\", \"r\") as f:",
        "    doc = json.loads(f)",
        "",
        "result_doc = {"
    ]
    for keyword, paths in matches.items():
        for path in paths:
            lines.append(f"    \"{keyword}\": doc{path_to_str(path)},")
    lines.append("}")
    return "\n".join(lines)

@CodeGeneratorRegistry.register('javascript')
def generate_extraction_code_js(matches: Dict[str, List[List[Union[str, int]]]]) -> str:
    """
    Generate JavaScript code to extract fields from a JSON object based on extracted paths.
    
    Args:
        matches (Dict[str, List[List[Union[str, int]]]]): Dictionary mapping keywords to their paths
        
    Returns:
        str: JavaScript code that extracts matching fields from the JSON object
    """
    lines = [
        "const fs = require('fs');",
        "",
        "const doc = JSON.parse(fs.readFileSync('<yourfilepath>.json', 'utf8'));",
        "",
        "const resultDoc = {"
    ]
    for keyword, paths in matches.items():
        for path in paths:
            path_str = "".join(f"['{p}']" if isinstance(p, str) else f"[{p}]" for p in path)
            lines.append(f"    '{keyword}': doc{path_str},")
    lines.append("};")
    return "\n".join(lines)

@CodeGeneratorRegistry.register('mysql')
def generate_extraction_code_mysql(matches: Dict[str, List[List[Union[str, int]]]]) -> str:
    """
    Generate MySQL code to extract fields from a JSON object based on extracted paths.
    
    Args:
        matches (Dict[str, List[List[Union[str, int]]]]): Dictionary mapping keywords to their paths
        
    Returns:
        str: MySQL code that extracts matching fields from the JSON object
    """
    lines = [
        "-- Assuming your JSON is stored in a column named 'json_data'",
        "SELECT"
    ]
    for keyword, paths in matches.items():
        for path in paths:
            path_str = "".join(f"->'$.{p}'" if isinstance(p, str) else f"->'$[{p}]'" for p in path)
            lines.append(f"    JSON_EXTRACT(json_data, '{path_str}') AS {keyword},")
    # Remove trailing comma from last line
    lines[-1] = lines[-1].rstrip(',')
    lines.append("FROM your_table;")
    return "\n".join(lines)

@CodeGeneratorRegistry.register('spark_sql')
def generate_extraction_code_spark_sql(matches: Dict[str, List[List[Union[str, int]]]]) -> str:
    """
    Generate Spark SQL code to extract fields from a JSON object based on extracted paths.
    
    Args:
        matches (Dict[str, List[List[Union[str, int]]]]): Dictionary mapping keywords to their paths
        
    Returns:
        str: Spark SQL code that extracts matching fields from the JSON object
    """
    lines = [
        "-- Assuming your JSON is stored in a column named 'json_data'",
        "SELECT"
    ]
    for keyword, paths in matches.items():
        for path in paths:
            path_str = "".join(f".{p}" if isinstance(p, str) else f"[{p}]" for p in path)
            lines.append(f"    get_json_object(json_data, '${path_str}') AS {keyword},")
    # Remove trailing comma from last line
    lines[-1] = lines[-1].rstrip(',')
    lines.append("FROM your_table;")
    return "\n".join(lines)

@CodeGeneratorRegistry.register('php')
def generate_extraction_code_php(matches: Dict[str, List[List[Union[str, int]]]]) -> str:
    """
    Generate PHP code to extract fields from a JSON object based on extracted paths.
    
    Args:
        matches (Dict[str, List[List[Union[str, int]]]]): Dictionary mapping keywords to their paths
        
    Returns:
        str: PHP code that extracts matching fields from the JSON object
    """
    lines = [
        "<?php",
        "",
        "$jsonString = file_get_contents('<yourfilepath>.json');",
        "$doc = json_decode($jsonString, true);",
        "",
        "$resultDoc = ["
    ]
    for keyword, paths in matches.items():
        for path in paths:
            path_str = "".join(f"['{p}']" if isinstance(p, str) else f"[{p}]" for p in path)
            lines.append(f"    '{keyword}' => $doc{path_str},")
    lines.append("];")
    return "\n".join(lines)

@CodeGeneratorRegistry.register('pyspark')
def generate_extraction_code_pyspark(matches: Dict[str, List[List[Union[str, int]]]]) -> str:
    """
    Generate PySpark code to extract fields from a JSON object based on extracted paths.
    
    Args:
        matches (Dict[str, List[List[Union[str, int]]]]): Dictionary mapping keywords to their paths
        
    Returns:
        str: PySpark code that extracts matching fields from the JSON object
    """
    lines = [
        "from pyspark.sql import SparkSession",
        "from pyspark.sql.functions import from_json, col",
        "",
        "# Initialize Spark session",
        "spark = SparkSession.builder.appName('JSONExtraction').getOrCreate()",
        "",
        "# Read JSON file",
        "df = spark.read.json('<yourfilepath>.json')",
        "",
        "# Extract fields"
    ]
    for keyword, paths in matches.items():
        for path in paths:
            path_str = "".join(f".{p}" if isinstance(p, str) else f"[{p}]" for p in path)
            lines.append(f"df = df.withColumn('{keyword}', col('{path_str}'))")
    
    lines.extend([
        "",
        "# Show results",
        "df.select(" + ", ".join(f"'{k}'" for k in matches.keys()) + ").show()"
    ])
    return "\n".join(lines)
