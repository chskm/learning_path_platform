# backend/main.py
from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
import mysql.connector
import bcrypt
import jwt
import httpx
import os
from typing import Optional

app = FastAPI()

# Environment variables (set by Elastic Beanstalk)
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret")
ML_API_URL = os.getenv("ML_API_URL")

# Database connection
def get_db():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database="learning_path_platform"
    )
    try:
        yield conn
    finally:
        conn.close()

# Pydantic models
class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    background: str

class UserLogin(BaseModel):
    email: str
    password: str

class GoalInput(BaseModel):
    goal: str
    experience: str

# Routes
@app.post("/register")
async def register(user: UserRegister, db: mysql.connector.MySQLConnection = Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    try:
        cursor.execute(
            "INSERT INTO users (name, email, password, background) VALUES (%s, %s, %s, %s)",
            (user.name, user.email, hashed_password.decode("utf-8"), user.background)
        )
        db.commit()
        return {"message": "User registered"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
    finally:
        cursor.close()

@app.post("/login")
async def login(user: UserLogin, db: mysql.connector.MySQLConnection = Depends(get_db)):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
    db_user = cursor.fetchone()
    cursor.close()
    if not db_user or not bcrypt.checkpw(user.password.encode("utf-8"), db_user["password"].encode("utf-8")):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt.encode({"id": db_user["id"]}, JWT_SECRET, algorithm="HS256")
    return {"token": token}

@app.post("/goals")
async def submit_goal(goal: GoalInput, authorization: Optional[str] = Header(None), db: mysql.connector.MySQLConnection = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user_id = payload["id"]
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT background FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        async with httpx.AsyncClient() as client:
            response = await client.post(ML_API_URL, json={
                "background": user["background"],
                "goal": goal.goal,
                "experience": goal.experience
            })
            response.raise_for_status()
            learning_path = response.json()["learning_path"]
        cursor.execute(
            "INSERT INTO goals (user_id, goal, experience, learning_path) VALUES (%s, %s, %s, %s)",
            (user_id, goal.goal, goal.experience, learning_path)
        )
        db.commit()
        cursor.close()
        return {"learning_path": learning_path}
    except (jwt.InvalidTokenError, httpx.HTTPError) as err:
        raise HTTPException(status_code=500, detail=str(err))