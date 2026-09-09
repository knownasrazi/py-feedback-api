from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import sqlite3, pathlib

DB = pathlib.Path("feedback.db")
app = FastAPI(title="py-feedback-api")

class Feedback(BaseModel):
    text: str
    type: str = "bug"

def init_db():
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS feedback (id INTEGER PRIMARY KEY, text TEXT, type TEXT)")
    con.close()

@app.post("/feedback")
def create_feedback(fb: Feedback):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("INSERT INTO feedback (text, type) VALUES (?, ?)", (fb.text, fb.type))
    con.commit()
    fid = cur.lastrowid
    con.close()
    return {"id": fid, "text": fb.text}

@app.get("/feedback", response_model=List[dict])
def list_feedback():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT id, text, type FROM feedback ORDER BY id DESC LIMIT 50")
    rows = [{"id": r[0], "text": r[1], "type": r[2]} for r in cur.fetchall()]
    con.close()
    return rows

@app.get("/health")
def health():
    return {"status": "ok"}

init_db()
