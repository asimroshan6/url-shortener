from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from database.session import get_db
from database.models import Click
from schemas.url import TopAnalyticsResponse


router = APIRouter(
    prefix="/analytics",
    tags=["Click Analytics Management"]
)



@router.get("/top", response_model=List[TopAnalyticsResponse])
def show_top_analytics(limit: int = 10, db: Session = Depends(get_db)):
    top_clicks = (
        db.query(
            Click.short_code, 
            func.count(Click.id).label("total_count")
        )
        .group_by(Click.short_code)
        .order_by(func.count(Click.id).desc())
        .limit(limit)
        .all()
    )
    
    return top_clicks
    
    

@router.get("/{code}")
def show_analytics(code: str, db: Session = Depends(get_db)):
    total_clicks = db.query(Click).filter(Click.short_code == code).count()

    if total_clicks == 0:
        raise HTTPException(status_code=404, detail="Short URL not found")

    return {
        "short_code": code,
        "total_clicks": total_clicks
    }
