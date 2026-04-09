from fastapi import FastAPI
from src.auth.router import router as auth_router
from src.articles.router import router as articles_router
from src.exceptions import register_exception_handlers


app = FastAPI()
app.include_router(auth_router)
app.include_router(articles_router)
register_exception_handlers(app)
