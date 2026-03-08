from database.session import Base
from sqlalchemy import String, Column, Integer, DateTime, func


class Url(Base):
    __tablename__ = "urls"
    
    id = Column(Integer, index=True, primary_key=True)
    original_url = Column(String)
    short_url = Column(String, index=True)

    
class Click(Base):
    __tablename__ = "clicks"
    
    id = Column(Integer, index=True, primary_key=True)
    short_code = Column(String, index=True)
    ip_address = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    user_agent = Column(String)
    