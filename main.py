from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import sqlite3

templates = Jinja2Templates(directory='simple-login-page/')
app = FastAPI()
class Database:
    
    def __init__(self):
        self.database = None
        
    # Create a function to create a user in the database
    async def create_user(self, username: str, password: str):
        async with self.database:
            query = f"INSERT INTO user (username, password)\
                VALUES ({username}, {password})"
            await self.database.execute(query)
            await self.database.commit()

    # Create  some test users
    async def create_test_users(self):
        await self.create_user('user1', 'password1')
        await self.create_user('user2', 'password2')

    @app.on_event('startup')
    async def startup(self):
        self.database = await sqlite3.connect('user.db')
        await self.create_test_users()

    # Define routes
    @app.get('/')
    async def read_form(self, request: Request):
        return templates.TemplateResponse("web.html", {"request": request})

    @app.post('/login')
    async def login(self, request: Request, username: str = Form(...), password: str = Form(...)):
        try:
            async with self.database: 
                user = await self.database.fetchone(f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'")
                
            if user:
                return templates.TemplateResponse("success.html", {"request": request, "username": username})
            else:
                return templates.TemplateResponse("failure.html", {"request": request})
        except:
            return templates.TemplateResponse("error.html", {"request": request})
        
    @app.on_event('shutdown')
    async def shutdown(self):
        await self.database.close()
