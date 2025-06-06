from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String
from database import Base

class Livro(Base):
    __tablename__ = 'livros'

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), index=True)
    autor = Column(String(100), index=True)
    editora = Column(String(100), index=True)
    genero = Column(String(100), index=True)
    ano_publicacao = Column(Integer, index=True)

class LivroCreate(BaseModel):
    titulo: str = Field(..., min_length=1)
    autor: str = Field(..., min_length=1)
    editora: str = Field(..., min_length=1)
    genero: str = Field(..., min_length=1)
    ano_publicacao: int

class LivroOut(LivroCreate):
    id: int

    class Config:
        orm_mode = True