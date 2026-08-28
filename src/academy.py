"""Hacking Academy LATAM - Plataforma de aprendizaje"""
from typing import Dict, List
from dataclasses import dataclass
from enum import Enum

class Difficulty(Enum):
    BEGINNER = "principiante"
    INTERMEDIATE = "intermedio"
    ADVANCED = "avanzado"
    EXPERT = "experto"

@dataclass
class Course:
    id: str
    title: str
    description: str
    difficulty: Difficulty
    duration_hours: int
    modules: List[str]
    price: float

@dataclass
class UserProgress:
    user_id: str
    course_id: str
    completed_modules: int
    total_modules: int
    score: float
    level: int

class HackingAcademy:
    def __init__(self):
        self.courses = self._load_courses()
        self.users = {}
    
    def _load_courses(self) -> List[Course]:
        return [
            Course("HA-001", "Fundamentos de Ciberseguridad", "Aprende los conceptos básicos de seguridad informática",
                  Difficulty.BEGINNER, 20, ["Intro a Seguridad", "Redes Básicas", "Criptografía", "Passwords Seguros"], 0),
            Course("HA-002", "Ethical Hacking Básico", "Introducción al hacking ético y penetración",
                  Difficulty.BEGINNER, 30, ["Reconocimiento", "Escaneo", "Enumeración", "Explotación Básica"], 49.99),
            Course("HA-003", "Pentesting Web", "Técnicas de penetración en aplicaciones web",
                  Difficulty.INTERMEDIATE, 40, ["OWASP Top 10", "SQL Injection", "XSS", "CSRF", "Auth Bypass"], 79.99),
            Course("HA-004", "Red Teaming", "Simulación de ataques avanzados",
                  Difficulty.ADVANCED, 50, ["Planning", "Initial Access", "Persistence", "Lateral Movement", "Exfiltration"], 149.99),
            Course("HA-005", "AI Security Specialist", "Seguridad de sistemas de inteligencia artificial",
                  Difficulty.EXPERT, 35, ["Prompt Injection", "Model Attacks", "Data Poisoning", "AI Red Teaming"], 199.99),
        ]
    
    def get_courses(self, difficulty: str = None) -> List[Course]:
        if difficulty:
            return [c for c in self.courses if c.difficulty.value == difficulty]
        return self.courses
    
    def get_course(self, course_id: str) -> Course:
        return next((c for c in self.courses if c.id == course_id), None)
    
    def enroll(self, user_id: str, course_id: str) -> bool:
        course = self.get_course(course_id)
        if not course:
            return False
        self.users[f"{user_id}_{course_id}"] = UserProgress(
            user_id=user_id, course_id=course_id,
            completed_modules=0, total_modules=len(course.modules),
            score=0, level=1
        )
        return True
    
    def complete_module(self, user_id: str, course_id: str, score: float) -> Dict:
        key = f"{user_id}_{course_id}"
        if key not in self.users:
            return {"error": "No inscrito"}
        progress = self.users[key]
        progress.completed_modules += 1
        progress.score = (progress.score + score) / 2
        if progress.completed_modules % 5 == 0:
            progress.level += 1
        return {"completed": progress.completed_modules, "total": progress.total_modules, "level": progress.level}
    
    def get_leaderboard(self) -> List[Dict]:
        sorted_users = sorted(self.users.values(), key=lambda x: x.score, reverse=True)[:10]
        return [{"user_id": u.user_id, "level": u.level, "score": round(u.score, 1)} for u in sorted_users]
    
    def get_stats(self) -> Dict:
        return {
            "total_courses": len(self.courses),
            "total_modules": sum(len(c.modules) for c in self.courses),
            "difficulty_levels": [d.value for d in Difficulty]
        }

academy = HackingAcademy()
