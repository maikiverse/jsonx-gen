from fastapi import FastAPI, Query, Request
from pydantic import BaseModel
from typing import List, Optional, Union, Dict, Any
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
import json
import logging
import traceback

from src.core import generate_extraction_code

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    mode: str = Query("match", enum=["match", "contains", "startswith", "endswith"]),
    type: str = Query("all", enum=["all", "key", "value"]),
    language: Optional[str] = Query(None)
):
    """
    Extract paths from JSON based on keywords and generate code.
    
    Args:
        request: The JSON object to analyze
        keywords: List of keywords to search for
        mode: Matching mode (match, contains, startswith, endswith)
        type: What to match (all, key, or value)
        language: Target language for code generation
        
    Returns:
        JSONResponse: Generated code
    """
    try:
        logger.info(f"Received request with keywords: {keywords}, mode: {mode}, type: {type}, language: {language}")

        code = generate_extraction_code(
            json_input=request.json_obj,
            keywords=keywords,
            mode=mode,
            type=type,
            target_language=language
        )
        return JSONResponse(content={"code": code})
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={"error": f"Invalid JSON: {str(e)}"}
        )
    except ValueError as e:
        logger.error(f"Value error: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Unexpected error: {str(e)}"}
        )