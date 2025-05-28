# JSON Extraction Code Generator

A command-line tool that generates code to extract specific fields from JSON documents based on keywords. The tool can generate extraction code in Python by default, and can also translate the code to other languages like MySQL or Spark SQL using OpenAI's API.

## Purpose

Data analysts often need to extract specific values from complex, unknown JSON structures. While the key or value to extract can be easily determined via text search in an editor, manually reconstructing the JSON path to the required field is cumbersome and error-prone.

This tool solves this problem by:
1. Automatically finding all paths to fields matching your keywords
2. Generating extraction code in Python
3. Optionally translating the code to other languages using an LLM

The key advantage is that sensitive data never leaves your environment. The tool first generates Python code locally, and only the generated code (not the data) is sent to the LLM for translation to other languages. This allows you to safely extract data from sensitive JSON structures without exposing company data to third parties.

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a configuration file:
   ```bash
   cp config.example .env
   ```
4. Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
   You can get your API key from: https://platform.openai.com/api-keys

## Usage

Basic usage:
```bash
python main.py --keywords KEYWORD1 KEYWORD2 [--mode MODE] [--language TARGET_LANGUAGE] JSON_INPUT
```

### Arguments:
- `--keywords`: One or more keywords to search for in the JSON
- `--mode`: (Optional) Matching mode for keywords:
  - `match`: Exact match (default)
  - `contains`: Substring match
  - `startswith`: Prefix match
- `--language`: (Optional) Target language for the extraction code. Defaults to 'python'. Can be set to other languages like 'mysql' or 'spark sql'
- `JSON_INPUT`: Path to a JSON file or a JSON string to analyze (must be the last argument)

### Examples:

Generate Python extraction code with exact matching:
```bash
python main.py --keywords name email --mode match data.json
```

Generate Python extraction code with substring matching:
```bash
python main.py --keywords name --mode contains '{"user": {"name": "John"}}'
```

Generate MySQL extraction code with prefix matching:
```bash
python main.py --keywords name email --language mysql --mode startswith data.json
```

Generate Spark SQL extraction code with exact matching:
```bash
python main.py --keywords name --language "spark sql" '{"user": {"name": "John"}}'
```

## Notes

- When using languages other than Python, the tool uses OpenAI's API to translate the generated Python code to the target language
- Make sure you have a valid OpenAI API key in your `.env` file when using non-Python languages
- The generated code will extract fields that match the provided keywords in both keys and values according to the specified matching mode
- The JSON input can be either a file path or a JSON string, and must be the last argument
- Your sensitive JSON data never leaves your environment - only the generated Python code is sent to the LLM for translation
- Exception: Sensitive Data in JSON-keys. Run with `--language python` first to review before translating to other languages