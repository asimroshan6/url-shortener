from pydantic import BaseModel, HttpUrl


class UrlInput(BaseModel):
    url: HttpUrl
    

class TopAnalyticsResponse(BaseModel):
    short_code: str
    total_count: int
    
    class Config:
        from_attributes = True