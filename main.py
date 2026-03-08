from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import redis.asyncio as redis
from contextlib import asynccontextmanager
from slowapi import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from database.session import Base, engine
from routers import url, analytics
from services.slow_api_client import limiter
from core.settings import settings

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # when app starts
    app.state.redis = redis.Redis.from_url(url=settings.REDIS_URL, decode_responses=True)
    
    yield
    
    # when app shout down
    await app.state.redis.close()


app = FastAPI(
    title="URL shortener app",
    description="A simple url shortener that user can paste a big url and can short and use that url",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_external_docs=None
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(router=url.router)
app.include_router(router=analytics.router)


# setting templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def show_hello(request: Request):
    return templates.TemplateResponse(request=request, name="home.html")

@app.get("/health")
async def health():
    return {"status": "ok"}
