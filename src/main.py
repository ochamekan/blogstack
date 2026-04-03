from fastapi import FastAPI

# from src.database import init_db
from src.auth.router import router as auth_router

app = FastAPI()
app.include_router(auth_router)


# @app.on_event("startup")
# def on_startup():
#     init_db()
