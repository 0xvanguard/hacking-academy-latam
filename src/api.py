"""Hacking Academy LATAM - API"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from academy import academy

app = FastAPI(title="Hacking Academy LATAM", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class EnrollRequest(BaseModel):
    user_id: str
    course_id: str

class CompleteRequest(BaseModel):
    user_id: str
    course_id: str
    score: float

@app.get("/")
async def root():
    return "<html><body><h1>🎓 Hacking Academy LATAM</h1><p>Aprende hacking ético en español con gamificación</p></body></html>"

@app.get("/api/courses")
async def get_courses(difficulty: Optional[str] = None):
    return [{"id": c.id, "title": c.title, "difficulty": c.difficulty.value, "duration": c.duration_hours, "price": c.price} for c in academy.get_courses(difficulty)]

@app.post("/api/enroll")
async def enroll(request: EnrollRequest):
    success = academy.enroll(request.user_id, request.course_id)
    return {"success": success, "message": "Inscripción exitosa" if success else "Curso no encontrado"}

@app.post("/api/complete")
async def complete(request: CompleteRequest):
    return academy.complete_module(request.user_id, request.course_id, request.score)

@app.get("/api/leaderboard")
async def leaderboard():
    return academy.get_leaderboard()

@app.get("/api/stats")
async def stats():
    return academy.get_stats()

if __name__ == "__main__":
    import uvicorn
    print("🎓 Iniciando Hacking Academy LATAM...")
    uvicorn.run(app, host="0.0.0.0", port=9008)
