from fastapi import Depends, FastAPI

from .advice import register_exception_handlers
from .event import lifespan
from .middleware import LoggingMiddleware
from .routers import youtube

app = FastAPI(lifespan=lifespan)

app.include_router(youtube.business_router)
app.include_router(youtube.end_point_router)

app.add_middleware(LoggingMiddleware)

register_exception_handlers(app)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
