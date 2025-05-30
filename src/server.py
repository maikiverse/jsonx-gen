from fastapi import FastAPI, Query, Request
from pydantic import BaseModel
from typing import List, Optional, Union, Dict, Any
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
import json
import logging
import traceback

from src.core import generate_extraction_code, parse_json_input

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


# Mount static files to /static instead of root
app.mount("/static", StaticFiles(directory="frontend"), name="static")

class ExtractionRequest(BaseModel):
    json_obj: Union[Dict[str, Any], List[Any], str]
    keywords: List[str]
    mode: str = "match"
    type: str = "all"
    language: Optional[str] = None

@app.get("/")
async def read_root():
    """Serve the main HTML page."""
    with open("frontend/index.html") as f:
        return HTMLResponse(content=f.read())

@app.post("/extract")
async def extract_post(request: ExtractionRequest):
    """
    Extract paths from JSON based on keywords and generate code (POST method).
    All parameters are in the request body.
    
    Args:
        request: The request containing JSON object and extraction parameters
        
    Returns:
        JSONResponse: Generated code
    """
    try:
        logger.info(f"Received POST request with keywords: {request.keywords}, mode: {request.mode}, type: {request.type}, language: {request.language}")
        logger.info(f"JSON input type: {type(request.json_obj).__name__}")

        code = generate_extraction_code(
            json_input=request.json_obj,
            keywords=request.keywords,
            mode=request.mode,
            type=request.type,
            target_language=request.language
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

@app.get("/extract")
async def extract_get(
    file_path: str = Query(...),
    keywords: str = Query(..., description="Comma-separated list of keywords"),
    mode: str = Query("match", enum=["match", "contains", "startswith", "endswith"]),
    type: str = Query("all", enum=["all", "key", "value"]),
    language: Optional[str] = Query(None)
):
    """
    Extract paths from JSON based on keywords and generate code (GET method).
    All parameters are in the query string.
    
    Args:
        file_path: Path to the JSON file or URL
        keywords: Comma-separated list of keywords to search for
        mode: Matching mode (match, contains, startswith, endswith)
        type: What to match (all, key, or value)
        language: Target language for code generation
        
    Returns:
        JSONResponse: Generated code
    """
    try:
        logger.info(f"Received GET request with file_path: {file_path}, keywords: {keywords}, mode: {mode}, type: {type}, language: {language}")
        
        # Parse keywords from comma-separated string
        keyword_list = [k.strip() for k in keywords.split(',')]

        code = generate_extraction_code(
            json_input=file_path,
            keywords=keyword_list,
            mode=mode,
            type=type,
            target_language=language
        )
        logger.info(f"Generated code: {code}")
        return JSONResponse(content={"code": code})
    except FileNotFoundError as e:
        logger.error(f"File not found: {str(e)}")
        return JSONResponse(
            status_code=404,
            content={"error": f"File not found: {str(e)}"}
        )
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