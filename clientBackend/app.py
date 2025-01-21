from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import jwt
import datetime
import aiomysql
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "db": os.getenv("MYSQL_DB"),
}

SECRET_KEY = os.getenv("SECRET_KEY")

# Pydantic models
class LoginRequest(BaseModel):
    username: str
    password: str

class Schedule(BaseModel):
    schedule_date: str
    schedule_description: str
    schedule_header: str
    user_id: Optional[int] = 1  # Default user_id

class EditScheduleRequest(BaseModel):
    schedule_description: str
    schedule_header: str

async def get_db():
    conn = await aiomysql.connect(**DB_CONFIG, cursorclass=aiomysql.DictCursor)
    try:
        yield conn
    finally:
        conn.close()

@app.post("/login")
async def login(request: LoginRequest, db=Depends(get_db)):
    async with db.cursor() as cursor:
        await cursor.execute("SELECT * FROM users WHERE username=%s", (request.username,))
        user = await cursor.fetchone()
        if not user:
            raise HTTPException(status_code=401, detail="Incorrect username")

        await cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (request.username, request.password))
        user = await cursor.fetchone()
        if user:
            token = jwt.encode({
                "user_id": user["id"],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }, SECRET_KEY, algorithm="HS256")
            return {"token": token}
        raise HTTPException(status_code=401, detail="Incorrect password")

@app.get("/users/{user_id}")
async def fetch_users(user_id: int, db=Depends(get_db)):
    async with db.cursor() as cursor:
        await cursor.execute("SELECT username FROM users WHERE id = %s", (user_id,))
        user = await cursor.fetchone()
        if user:
            return user
        raise HTTPException(status_code=404, detail="User not found")

@app.get("/schedules")
async def fetch_schedules(db=Depends(get_db)):
    async with db.cursor() as cursor:
        await cursor.execute("SELECT * FROM schedules")
        rows = await cursor.fetchall()
        return rows

@app.post("/addschedules")
async def add_schedule(schedule: Schedule, db=Depends(get_db)):
    async with db.cursor() as cursor:
        await cursor.execute(
            "INSERT INTO schedules (schedule_date, schedule_description, schedule_header, user_id) VALUES (%s, %s, %s, %s)",
            (schedule.schedule_date, schedule.schedule_description, schedule.schedule_header, schedule.user_id)
        )
        await db.commit()
        return {"message": "Schedule added successfully"}

@app.put("/editschedules/{schedule_id}")
async def edit_schedule(schedule_id: int, request: EditScheduleRequest, db=Depends(get_db)):
    async with db.cursor() as cursor:
        await cursor.execute(
            "UPDATE schedules SET schedule_description=%s, schedule_header=%s WHERE id=%s",
            (request.schedule_description, request.schedule_header, schedule_id)
        )
        await db.commit()
        return {"message": "Schedule updated successfully"}

@app.delete("/deleteschedules/{schedule_id}")
async def delete_schedule(schedule_id: int, db=Depends(get_db)):
    async with db.cursor() as cursor:
        await cursor.execute("DELETE FROM schedules WHERE id = %s", (schedule_id,))
        await db.commit()
        return {"message": "Schedule deleted successfully"}
