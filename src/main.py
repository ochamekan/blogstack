from fastapi import FastAPI
from src.exceptions import register_exception_handlers
from src.auth.router import router as auth_router
from src.articles.router import router as articles_router
from src.tags.router import router as tags_router
from src.article_tags.router import router as article_tags_router
from src.claps.router import router as claps_router


app = FastAPI()
app.include_router(auth_router)
app.include_router(articles_router)
app.include_router(tags_router)
app.include_router(article_tags_router)
app.include_router(claps_router)

register_exception_handlers(app)
