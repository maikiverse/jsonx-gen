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
            json_path = '$' + ''.join(
                f"[{p}]" if isinstance(p, int) else f".{p}" for p in path
            )
            lines.append(f"    JSON_UNQUOTE(JSON_EXTRACT(json_data, '{json_path}')) AS {keyword},")

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


@CodeGeneratorRegistry.register('postgresql')
def generate_extraction_code_postgresql(matches: Dict[str, List[List[Union[str, int]]]]) -> str:
    lines = [
        "-- Assuming json_data is a JSONB column",
        "SELECT"
    ]
    for keyword, paths in matches.items():
        for path in paths:
            json_path = "{" + ",".join([str(p) if isinstance(p, int) else p for p in path]) + "}"
            lines.append(f"    json_data #>> '{json_path}' AS \"{keyword}\",")
    lines[-1] = lines[-1].rstrip(',')
    lines.append("FROM your_table;")
    return "\n".join(lines)

@CodeGeneratorRegistry.register('java')
def generate_extraction_code_java(matches: Dict[str, List[List[Union[str, int]]]]) -> str:
    lines = [
        "import org.json.JSONObject;",
        "import java.nio.file.*;",
        "",
        "String content = Files.readString(Path.of(\"<yourfilepath>.json\"));",
        "JSONObject doc = new JSONObject(content);",
        "",
        "JSONObject resultDoc = new JSONObject();"
    ]
    for keyword, paths in matches.items():
        for path in paths:
            access = ".".join([f"getJSONObject(\"{p}\")" if isinstance(p, str) else f"getJSONArray().get({p})" for p in path[:-1]])
            final = f"get(\"{path[-1]}\")" if isinstance(path[-1], str) else f"get({path[-1]})"
            lines.append(f'resultDoc.put("{keyword}", doc.{access}.{final});')
    return "\n".join(lines)

@CodeGeneratorRegistry.register('c++')
def generate_extraction_code_cpp(matches: Dict[str, List[List[Union[str, int]]]]) -> str:
    lines = [
        "#include <nlohmann/json.hpp>",
        "#include <fstream>",
        "",
        "std::ifstream i(\"<yourfilepath>.json\");",
        "nlohmann::json doc;",
        "i >> doc;",
        "",
        "nlohmann::json resultDoc;"
    ]
    for keyword, paths in matches.items():
        for path in paths:
            cpp_path = "".join([f"[{json.dumps(p)}]" for p in path])
            lines.append(f'resultDoc["{keyword}"] = doc{cpp_path};')
    return "\n".join(lines)

@CodeGeneratorRegistry.register('c#')
def generate_extraction_code_csharp(matches: Dict[str, List[List[Union[str, int]]]]) -> str:
    lines = [
        "using Newtonsoft.Json.Linq;",
        "var json = File.ReadAllText(\"<yourfilepath>.json\");",
        "var doc = JObject.Parse(json);",
        "var resultDoc = new JObject();"
    ]
    for keyword, paths in matches.items():
        for path in paths:
            access = "".join([f"[\"{p}\"]" if isinstance(p, str) else f"[{p}]" for p in path])
            lines.append(f'resultDoc["{keyword}"] = doc{access};')
    return "\n".join(lines)

@CodeGeneratorRegistry.register('go')
def generate_extraction_code_go(matches: Dict[str, List[List[Union[str, int]]]]) -> str:
    lines = [
        "import (",
        "    \"encoding/json\"",
        "    \"os\"",
        ")",
        "",
        "var doc map[string]interface{}",
        "file, _ := os.ReadFile(\"<yourfilepath>.json\")",
        "json.Unmarshal(file, &doc)",
        "",
        "resultDoc := map[string]interface{}{}"
    ]
    for keyword, paths in matches.items():
        for path in paths:
            access = "".join([f"[\"{p}\"]" if isinstance(p, str) else f"[{p}]" for p in path])
            lines.append(f'resultDoc["{keyword}"] = doc{access}')
    return "\n".join(lines)

@CodeGeneratorRegistry.register('rust')
def generate_extraction_code_rust(matches: Dict[str, List[List[Union[str, int]]]]) -> str:
    lines = [
        "use serde_json::Value;",
        "use std::fs;",
        "",
        "let data = fs::read_to_string(\"<yourfilepath>.json\").unwrap();",
        "let doc: Value = serde_json::from_str(&data).unwrap();",
        "",
        "let mut result_doc = serde_json::Map::new();"
    ]
    for keyword, paths in matches.items():
        for path in paths:
            access = "".join([f"[\"{p}\"]" if isinstance(p, str) else f"[{p}]" for p in path])
            lines.append(f'result_doc.insert("{keyword}".to_string(), doc{access}.clone());')
    return "\n".join(lines)

@CodeGeneratorRegistry.register('shell')
def generate_extraction_code_shell(matches: Dict[str, List[List[Union[str, int]]]]) -> str:
    lines = [
        "#!/bin/bash",
        "",
        "jq '"
    ]
    filters = []
    for keyword, paths in matches.items():
        for path in paths:
            jq_path = "." + "".join([f".{p}" if isinstance(p, str) else f"[{p}]" for p in path])
            filters.append(f"\"{keyword}\": {jq_path}")
    lines.append("{ " + ", ".join(filters) + " }'")
    lines.append("<yourfilepath>.json")
    return "\n".join(lines)

@CodeGeneratorRegistry.register('ruby')
def generate_extraction_code_ruby(matches: Dict[str, List[List[Union[str, int]]]]) -> str:
    lines = [
        "require 'json'",
        "",
        "doc = JSON.parse(File.read('<yourfilepath>.json'))",
        "result_doc = {}"
    ]
    for keyword, paths in matches.items():
        for path in paths:
            access = "".join([f"['{p}']" if isinstance(p, str) else f"[{p}]" for p in path])
            lines.append(f'result_doc["{keyword}"] = doc{access}')
    return "\n".join(lines)

@CodeGeneratorRegistry.register('r')
def generate_extraction_code_r(matches: Dict[str, List[List[Union[str, int]]]]) -> str:
    lines = [
        "library(jsonlite)",
        "doc <- fromJSON('<yourfilepath>.json')",
        "result_doc <- list()"
    ]
    for keyword, paths in matches.items():
        for path in paths:
            access = "".join([f"[['{p}']]" if isinstance(p, str) else f"[[{p+1}]]" for p in path])
            lines.append(f'result_doc[["{keyword}"]] <- doc{access}')
    return "\n".join(lines)

@CodeGeneratorRegistry.register('matlab')
def generate_extraction_code_matlab(matches: Dict[str, List[List[Union[str, int]]]]) -> str:
    lines = [
        "fid = fopen('<yourfilepath>.json');",
        "raw = fread(fid, inf);",
        "str = char(raw');",
        "fclose(fid);",
        "doc = jsondecode(str);",
        "result_doc = struct();"
    ]
    for keyword, paths in matches.items():
        for path in paths:
            access = "".join([f".{p}" if isinstance(p, str) else f"({p+1})" for p in path])
            lines.append(f'result_doc.{keyword} = doc{access};')
    return "\n".join(lines)

@CodeGeneratorRegistry.register('mongodb')
def generate_extraction_code_mongodb(matches: Dict[str, List[List[Union[str, int]]]]) -> str:
    lines = [
        "// MongoDB aggregation pipeline to project specific fields",
        "db.your_collection.aggregate([",
        "  {",
        "    $project: {"
    ]
    for keyword, paths in matches.items():
        for path in paths:
            dot_path = "".join([f".{p}" if isinstance(p, str) else f".{p}" for p in path])[1:]
            lines.append(f"      {json.dumps(keyword)}: '${dot_path}',")
    if lines[-1].endswith(','):
        lines[-1] = lines[-1].rstrip(',')
    lines.append("    }")
    lines.append("  }")
    lines.append("])")
    return "\n".join(lines)