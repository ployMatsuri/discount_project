from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import json
from discount_logic import apply_discounts
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/calculate")
async def calculate(file: UploadFile = File(...)):
    contents = await file.read()
    try:
        data = json.loads(contents)
        result = apply_discounts(data)
        if "error" in result:
            return JSONResponse(result, status_code=400)
        return JSONResponse(result)
    except json.JSONDecodeError:
        return JSONResponse({"error": "Invalid JSON format"}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)
