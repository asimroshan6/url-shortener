from fastapi import APIRouter, Request, BackgroundTasks
from fastapi import Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database.models import Url
from database.session import get_db, SessionLocal
from schemas.url import UrlInput
from services.enc_base62 import encode_base62
from services.redis_client import get_redis
from services.slow_api_client import limiter
from services.analytics_service import save_click

router = APIRouter(tags=["URL Management"])



@router.post("/generate/")
@limiter.limit("5/minute")
async def parse_url(url_input: UrlInput, request: Request,db: Session = Depends(get_db)):
    try:
        url = Url(original_url=str(url_input.url))
        db.add(url)
        db.commit()
        db.refresh(url)
        
        short_code = encode_base62(num=url.id)
        url.short_url = f"127.0.0.1:8000/{short_code}"
        db.commit()

        return {"original_url": url.original_url, "short_url": url.short_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred {e}")


@router.get("/{code}/")
@limiter.limit("50/minute")
async def redirect(code: str, request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    
    ip = request.client.host
    user_agent = request.headers.get("user-agent")
    
    background_tasks.add_task(
        save_click,
        SessionLocal,
        code,
        ip,
        user_agent
    )
    
    redis_client = get_redis(request)
    cached_url = await redis_client.get(code)
    
    if cached_url:
        return RedirectResponse(url=cached_url)
        
    url = db.query(Url).filter(Url.short_url == f"127.0.0.1:8000/{code}").first()
    if url:
        await redis_client.setex(code, 3600, url.original_url)
        return RedirectResponse(url=url.original_url)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL not found")