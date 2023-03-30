from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import sqlite3

templates = Jinja2Templates(directory='templates/')
app = FastAPI()
class Database:
    
    def __init__(self, path):
        self.database = sqlite3.connect(path)
        self.cursor = self.database.cursor()
        
    # Create a function to create a user in the database
    def create_user(self, user: str, pw: str):
        query = """INSERT INTO user VALUES (?, ?)"""
        print(query)
        self.cursor.execute(query, (user, pw))

    # Create  some test users
    def create_test_users(self):
        self.create_user('user1', 'password1')

path = 'user.db'


@app.on_event('startup')
async def startup():
    global database
    database = Database(path)
    database.create_test_users()

# Define routes
@app.get('/')
async def read_form(request: Request):
    return templates.TemplateResponse("web.html", {"request": request})

@app.post('/login')
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    try:
        async with database: 
            user = await database.fetchone(f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'")
            
        if user:
            return templates.TemplateResponse("success.html", {"request": request, "username": username})
        else:
            return templates.TemplateResponse("failure.html", {"request": request})
    except:
        return templates.TemplateResponse("error.html", {"request": request})
    
@app.on_event('shutdown')
async def shutdown():
    await database.close()
