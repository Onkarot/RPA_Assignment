import os
import logging

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.concurrency import run_in_threadpool
from pydantic import BaseModel, Field
from automation import run_automation

app = FastAPI(title="RPA Automation")

os.makedirs("output", exist_ok=True)
os.makedirs("logs", exist_ok=True)
os.makedirs("screenshots", exist_ok=True)

logging.basicConfig(filename="logs/info.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class AutomationRequest(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=100)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    employee_id: str = Field(min_length=1, max_length=100)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"request": request})

@app.post("/submit")
async def submit_form(form_data: AutomationRequest):
    try:
        result = await run_in_threadpool(run_automation, form_data.model_dump())
        return {"message": result["message"], "result": result}
    except Exception as e:
        logging.error(f"Error during automation: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during automation.")