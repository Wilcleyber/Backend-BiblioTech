from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import crud, models
from .database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],            
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/livros", response_model=list[models.LivroOut])
def listar_livros(db: Session = Depends(get_db)):
    return crud.get_livros(db)

@app.get("/livros/{livro_id}", response_model=models.LivroOut)
def buscar_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = crud.get_livro_by_id(db, livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Book not found")
    return livro

@app.post("/livros", response_model=models.LivroOut)
def adicionar_livro(livro: models.LivroCreate, db: Session = Depends(get_db)):
    return crud.create_livro(db, livro)

@app.put("/livros/{livro_id}", response_model=models.LivroOut)
def atualizar_livro(livro_id: int, livro: models.LivroCreate, db: Session = Depends(get_db)):
    livro_atualizado = crud.update_livro(db, livro_id, livro)
    if not livro_atualizado:
        raise HTTPException(status_code=404, detail="Book not found")
    return livro_atualizado

@app.delete("/livros/{livro_id}", response_model=models.LivroOut)
def deletar_livro(livro_id: int, db:Session = Depends(get_db)):
    livro_deletado = crud.delete_livro(db, livro_id)
    if not livro_deletado:
        raise HTTPException(status_code=404, detail="Book not found")
    return livro_deletado