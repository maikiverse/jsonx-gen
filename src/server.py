from fastapi import FastAPI, Query, Request
from pydantic import BaseModel
from typing import List, Optional, Union, Dict, Any
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path

from src.core import generate_extraction_code

app = FastAPI()


# Mount static files to /static instead of root
app.mount("/static", StaticFiles(directory="frontend"), name="static")

class ExtractionRequest(BaseModel):
    json_obj: Union[Dict[str, Any], List[Any], str]

@app.get("/")
async def read_root():
    """Serve the main HTML page."""
    with open("frontend/index.html") as f:
        return HTMLResponse(content=f.read())

@app.post("/extract")
async def extract(
    request: ExtractionRequest,
    keywords: List[str] = Query(...),
    mode: str = Query("match", enum=["match", "contains", "startswith"]),
    language: Optional[str] = Query(None)
):
    """
    Extract paths from JSON based on keywords and generate code.
    
    Args:
        request: The JSON object to analyze
        keywords: List of keywords to search for
        mode: Matching mode (match, contains, startswith)
        language: Target language for code generation
        
    Returns:
        JSONResponse: Generated code
    """
    try:
        code = generate_extraction_code(
            json_input=request.json_obj,
            keywords=keywords,
            mode=mode,
            target_language=language
        )
        return JSONResponse(content={"code": code})
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )