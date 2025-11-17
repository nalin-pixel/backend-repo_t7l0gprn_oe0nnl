import os
import random
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import create_document, get_documents, db
from schemas import Task as TaskSchema, Note as NoteSchema

app = FastAPI(title="MentorAI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "MentorAI API is running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from MentorAI backend"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = getattr(db, 'name', "✅ Connected")
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# -------------------- Motivation --------------------
MOTIVATION_POOL = [
    ("Ogni giorno è una nuova opportunità per diventare la versione migliore di te.", "MentorAI"),
    ("Fai oggi ciò che altri non vogliono, domani vivrai come altri non possono.", "Anonimo"),
    ("La disciplina batte la motivazione.", "MentorAI"),
    ("Picchi piccoli, costanza grande: il progresso è la somma di passi minuscoli.", "MentorAI"),
    ("Il successo è l’abitudine di fare bene le piccole cose.", "MentorAI"),
]

class MotivationOut(BaseModel):
    text: str
    author: Optional[str] = None

@app.get("/api/motivation", response_model=MotivationOut)
def get_motivation():
    text, author = random.choice(MOTIVATION_POOL)
    return {"text": text, "author": author}

# -------------------- Tasks --------------------
@app.post("/api/tasks")
def create_task(task: TaskSchema):
    inserted_id = create_document("task", task)
    return {"ok": True, "id": inserted_id}

@app.get("/api/tasks")
def list_tasks(limit: int = Query(20, ge=1, le=200)):
    docs = get_documents("task", {}, limit)
    # Convert ObjectId to string for frontend safety
    for d in docs:
        if "_id" in d:
            d["id"] = str(d.pop("_id"))
    return {"items": docs}

# -------------------- Notes --------------------
@app.post("/api/notes")
def create_note(note: NoteSchema):
    inserted_id = create_document("note", note)
    return {"ok": True, "id": inserted_id}

@app.get("/api/notes")
def list_notes(limit: int = Query(20, ge=1, le=200)):
    docs = get_documents("note", {}, limit)
    for d in docs:
        if "_id" in d:
            d["id"] = str(d.pop("_id"))
    return {"items": docs}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
