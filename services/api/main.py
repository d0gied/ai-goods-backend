import fastapi
from api.routers import users, tasks


app = fastapi.FastAPI()

app.include_router(users.router)
app.include_router(tasks.router)

