"""Hacking Academy LATAM - API Completa"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from academy import academy

app = FastAPI(title="Hacking Academy LATAM", version="2.0.0",
              description="Plataforma de aprendizaje de hacking ético gamificada en español")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ==================== MODELS ====================

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

class EnrollRequest(BaseModel):
    user_id: str
    course_id: str

class CompleteModuleRequest(BaseModel):
    user_id: str
    course_id: str
    module_id: str

class LabSubmitRequest(BaseModel):
    user_id: str
    lab_id: str
    flag: str

class XpRequest(BaseModel):
    user_id: str
    amount: int

# ==================== ROUTES ====================

@app.get("/")
async def root():
    return FileResponse("docs/index.html")

@app.get("/api/stats")
async def stats():
    return academy.get_stats()

@app.get("/api/courses")
async def courses(difficulty: Optional[str] = None):
    return academy.get_courses(difficulty)

@app.get("/api/courses/{course_id}")
async def course_detail(course_id: str):
    c = academy.get_course(course_id)
    if not c:
        raise HTTPException(404, "Curso no encontrado")
    return c

@app.post("/api/register")
async def register(req: RegisterRequest):
    return academy.register(req.username, req.email, req.password)

@app.post("/api/login")
async def login(req: LoginRequest):
    return academy.login(req.username, req.password)

@app.get("/api/users/{user_id}")
async def user_profile(user_id: str):
    u = academy.get_user(user_id)
    if not u:
        raise HTTPException(404, "Usuario no encontrado")
    return u

@app.post("/api/enroll")
async def enroll(req: EnrollRequest):
    return academy.enroll(req.user_id, req.course_id)

@app.post("/api/complete-module")
async def complete_module(req: CompleteModuleRequest):
    return academy.complete_module(req.user_id, req.course_id, req.module_id)

@app.post("/api/labs/submit")
async def submit_lab(req: LabSubmitRequest):
    return academy.complete_lab(req.user_id, req.lab_id, req.flag)

@app.get("/api/labs")
async def labs(category: Optional[str] = None, difficulty: Optional[str] = None):
    return academy.get_labs(category, difficulty)

@app.get("/api/labs/{lab_id}")
async def lab_detail(lab_id: str):
    lab = next((l for l in academy.labs if l.id == lab_id), None)
    if not lab:
        raise HTTPException(404, "Lab no encontrado")
    return {
        "id": lab.id, "title": lab.title, "description": lab.description,
        "difficulty": lab.difficulty.value, "category": lab.category,
        "xp_reward": lab.xp_reward, "hints": lab.hints,
    }

@app.get("/api/leaderboard")
async def leaderboard(country: Optional[str] = None):
    return academy.get_leaderboard(country)

@app.get("/api/missions")
async def missions():
    return academy.get_missions()

@app.get("/api/badges")
async def badges():
    return academy.get_badges()

@app.post("/api/add-xp")
async def add_xp(req: XpRequest):
    return academy.add_xp(req.user_id, req.amount)

if __name__ == "__main__":
    import uvicorn
    print("🎓 Iniciando Hacking Academy LATAM v2.0...")
    uvicorn.run(app, host="0.0.0.0", port=9008)
