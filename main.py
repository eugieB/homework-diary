from fastapi import FastAPI, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from supabase import create_client, Client
import os

SUPABASE_URL   = os.getenv("SUPABASE_URL")
SUPABASE_KEY   = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- Pages -------------------------------------------------------------

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# --- Teacher API -------------------------------------------------------

@app.post("/api/homework")
def add_homework(date: str = Form(...),
                 subject: str = Form(...),
                 task: str = Form(...),
                 learner_id: str = Form(...)):
    supabase.table("homework").insert({
        "date": date,
        "subject": subject,
        "task": task,
        "learner_id": learner_id
    }).execute()
    return {"status": "added"}

# --- Progress API ------------------------------------------------------

@app.get("/api/progress/{learner_id}")
def progress(learner_id: str):
    rows = supabase.table("homework").select("*").eq("learner_id", learner_id).execute()
    return rows.data
