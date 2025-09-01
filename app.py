from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from models import Base, School, Learner, Homework, Analytics
import uvicorn

engine = create_engine("sqlite:///./homework.db", connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def dashboard(request: Request, db: Session = next(get_db())):
    hw = db.query(Homework).order_by(Homework.date.desc()).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "hw": hw})

@app.post("/add")
def add(request: Request,
        task: str = Form(...),
        learner: str = Form(...),
        focus: str = Form(...),
        db: Session = next(get_db())):
    l = db.query(Learner).filter_by(name=learner).first()
    if not l:
        l = Learner(name=learner, school_id=1)
        db.add(l); db.commit()
    db.add(Homework(task=task, special_focus=focus, learner_id=l.id))
    db.commit()
    return {"ok": True}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
