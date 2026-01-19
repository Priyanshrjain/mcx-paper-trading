from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, engine
import models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="MCX Paper Trading API")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"status": "MCX Paper Trading Backend Running"}


@app.post("/trade")
def place_trade(trade: schemas.TradeCreate, db: Session = Depends(get_db)):
    new_trade = models.Trade(**trade.dict())
    db.add(new_trade)
    db.commit()
    db.refresh(new_trade)
    return new_trade


@app.get("/trades/{user_id}")
def get_trades(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Trade).filter(models.Trade.user_id == user_id).all()
