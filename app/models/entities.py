from sqlalchemy import Column, Integer, String, Text, ForeignKey
from pgvector.sqlalchemy import Vector

from app.core.database import Base

class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    
    id =  Column(Integer, primary_key=True, index= True)
    
    document_name = Column(String, nullable=False)
    
    chunk_index = Column(Integer,nullable=False)
    
    content = Column(Text, nullable=False)
    
    embedding = Column(Vector(384))
    
    page_number = Column(Integer, nullable=True)

    source_type = Column(String, nullable=True)

    source_url = Column(String, nullable=True)

    document_name = Column(String, nullable=True)
    