from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import sqlite3


templates = Jinja2Templates(directory='templates/')
app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "static"),
    name="static",
)

@app.get('/')
async def login(request: Request):
    return templates.TemplateResponse("web.html", {"request": request})

@app.post('/login')
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    try:
        conn = sqlite3.connect("user.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        print(user)
        if user:
            return templates.TemplateResponse("success.html", {"request": request, "username": username})
        else:
            return templates.TemplateResponse("failure.html", {"request": request})
    except Exception:
        print(Exception)
        return templates.TemplateResponse("error.html", {"request": request})   
    
@app.get("/register")
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(request: Request, username: str = Form(...), password: str = Form(...)):
    conn = sqlite3.connect("user.db")
    c = conn.cursor()
    c.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

    return templates.TemplateResponse("success-register.html", {"request": request, "username": username})