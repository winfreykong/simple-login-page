from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import sqlite3

templates = Jinja2Templates(directory='templates/')
app = FastAPI()

@app.get('/')
async def read_form(request: Request):
    return templates.TemplateResponse("web.html", {"request": request})

@app.post('/login')
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    cursor = conn.cursor()
    try:
        async with conn: 
            user = await cursor.fetchone(f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'")
            
        if user:
            return templates.TemplateResponse("success.html", {"request": request, "username": username})
        else:
            return templates.TemplateResponse("failure.html", {"request": request})
    except:
        return templates.TemplateResponse("error.html", {"request": request})   


async def create_user(conn, user: str, pw: str): 
    cursor = conn.cursor()
    query = """INSERT INTO user(username, password) VALUES (?, ?)"""
    cursor.execute(query, (user, pw))
    cursor.close()

async def create_test_users(conn):
    await create_user(conn, 'user1', 'testingtesttest')

@app.on_event('startup')
async def startup():
    global conn
    conn = sqlite3.connect('user.db')
    await create_test_users(conn)


    
@app.on_event('shutdown')
async def shutdown():
    await conn.close()
