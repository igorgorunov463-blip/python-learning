from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import sqlite3

# Создаем приложение
app = FastAPI(title="Мой Первый Стартап")

# Подключаем папку с HTML-шаблонами
templates = Jinja2Templates(directory="templates")

# Функция для подключения к базе
def get_db_connection():
    conn = sqlite3.connect("startup.db")
    conn.row_factory = sqlite3.Row
    return conn

# --- МАРШРУТЫ API ---

@app.get("/")
def read_root():
    return {"message": "Привет! Это API моего будущего стартапа."}

@app.get("/users")
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    
    # Возвращаем JSON с правильной кодировкой
    return JSONResponse(
        content={"users": [dict(row) for row in users]},
        media_type="application/json; charset=utf-8"
    )

@app.get("/users/{user_id}")
def get_user(user_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return JSONResponse(
            content={"user": dict(user)},
            media_type="application/json; charset=utf-8"
        )
    return {"error": "Пользователь не найден"}

# --- МОДЕЛИ ДЛЯ РЕГИСТРАЦИИ ---
class UserCreate(BaseModel):
    name: str
    email: str
    role: str = "user"

@app.post("/users")
def create_user(user: UserCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (name, email, role) VALUES (?, ?, ?)", 
            (user.name, user.email, user.role)
        )
        conn.commit()
        return {"message": f"Пользователь {user.name} успешно создан!"}
    except sqlite3.IntegrityError:
        return {"error": "Этот email уже занят"}
    finally:
        conn.close()

# --- МАРШРУТ ДЛЯ САЙТА (HTML) ---

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")