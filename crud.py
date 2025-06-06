from sqlalchemy.orm import Session
import models

def get_livros(db: Session, skip: int = 0, limit: int = 30):
    return db.query(models.Livro).offset(skip).limit(limit).all()

def get_livro_by_id(db: Session, livro_id: int):
    return db.query(models.Livro).filter(models.Livro.id == livro_id).first()

def create_livro(db: Session, livro: models.LivroCreate):
    try:
        db_livro = models.Livro(**livro.dict())
        db.add(db_livro)
        db.commit()
        db.refresh(db_livro)
        return db_livro
    except Exception as e:
        db.rollback()
        raise e

def update_livro(db: Session, livro_id: int, livro: models.LivroCreate):
    try:
        db_livro = get_livro_by_id(db, livro_id)
        if db_livro:
            for field, value in livro.dict().items():
                setattr(db_livro, field, value)
            db.commit()
            db.refresh(db_livro)
        return db_livro
    except Exception as e:
        db.rollback()
        raise e

def delete_livro(db: Session, livro_id: int):
    try:
        db_livro = get_livro_by_id(db, livro_id)
        if db_livro:
            db.delete(db_livro)
            db.commit()
        return db_livro
    except Exception as e:
        db.rollback()
        raise e



    