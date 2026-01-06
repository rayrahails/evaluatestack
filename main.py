from fastapi import FastAPI, HTTPException
from typing import Dict
import asyncio

app = FastAPI()

# Global in-memory "database"
users: Dict[str, dict] = {}


@app.post("/register")
async def register_user(username: str, password: str, metadata: dict | None = None):
    if username in users:
        raise HTTPException(status_code=409, detail="User already exists")

    users[username] = {
        "username": username,
        "password": password,
        "metadata": metadata if metadata is not None else {}
    }

    await asyncio.sleep(1)

    return {"message": "User created"}


@app.post("/login")
async def login(username: str, password: str):
    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")

    user = users[username]

    if user["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid password")

    return {"message": "Logged in"}


@app.get("/users/{username}")
async def get_user(username: str):
    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")

    return users[username]


@app.post("/users/{username}/update")
async def update_user(username: str, data: dict):
    if username not in users:
        raise HTTPException(status_code=404, detail="User not found")

    users[username].update(data)

    return {"message": "User updated"}
