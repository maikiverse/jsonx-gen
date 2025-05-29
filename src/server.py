"""
FastAPI server for JSON extraction code generation.
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from .core import generate_extraction_code

app = FastAPI(
    title="JSONXGen API",
    description="API for generating extraction code from JSON schemas",
    version="0.1.0"
)

class JsonInput(BaseModel):
    """
    Request model for JSON input.
    """
    json_input: str = Field(
        default='{"metadata": {"version": "1.0", "created_at": "2024-03-20", "keyword1": "metadata_value"}}',
        description="JSON string or file path to analyze"
    )

@app.post("/generate")
async def generate_code(
    request: JsonInput,
    keywords: List[str] = Query(
        default=["keyword1", "keyword2"],
        description="List of keywords to search for in the JSON structure"
    ),
    mode: str = Query(
        default="match",
        description="Matching mode: 'match' (exact), 'contains' (substring), or 'startswith' (prefix)",
        choices=["match", "contains", "startswith"]
    ),
    language: str = Query(
        default="python",
        description="Target programming language for the generated code",
        examples=["python", "mysql", "spark sql", "php", "pyspark"]
    )
):
    """
    Generate extraction code from JSON input.
    
    Args:
        request: JsonInput containing the JSON string or file path
        keywords: List of keywords to search for
        mode: Matching mode for keywords
        language: Target programming language
        
    Returns:
        dict: Generated code
        
    Raises:
        HTTPException: If there's an error processing the request
    """
    try:
        code = generate_extraction_code(
            request.json_input,
            keywords,
            mode,
            language
        )
        return {"code": code}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "JSONXGen API",
        "version": "0.1.0",
        "description": "API for generating extraction code from JSON schemas",
        "endpoints": {
            "/generate": "POST - Generate extraction code",
            "/docs": "GET - API documentation (Swagger UI)",
            "/redoc": "GET - API documentation (ReDoc)"
        }
    } 