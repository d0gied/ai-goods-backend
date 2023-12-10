import fastapi
from api.config import HOST, PORT
from api.routers import parse, search

app = fastapi.FastAPI()

app.include_router(search.router)
app.include_router(parse.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
