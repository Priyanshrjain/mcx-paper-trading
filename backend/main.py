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

@app.get("/portfolio/{user_id}")
def get_portfolio(user_id: int, db: Session = Depends(get_db)):
    trades = db.query(models.Trade).filter(
        models.Trade.user_id == user_id
    ).all()

    portfolio = {}

    for trade in trades:
        if trade.commodity not in portfolio:
            portfolio[trade.commodity] = {
                "buy_lots": 0,
                "sell_lots": 0,
                "buy_value": 0.0,
                "sell_value": 0.0
            }

        if trade.side == "BUY":
            portfolio[trade.commodity]["buy_lots"] += trade.lots
            portfolio[trade.commodity]["buy_value"] += trade.price * trade.lots
        else:
            portfolio[trade.commodity]["sell_lots"] += trade.lots
            portfolio[trade.commodity]["sell_value"] += trade.price * trade.lots

    result = {}

    for commodity, data in portfolio.items():
        net_lots = data["buy_lots"] - data["sell_lots"]
        avg_buy_price = (
            data["buy_value"] / data["buy_lots"]
            if data["buy_lots"] > 0 else 0
        )

        result[commodity] = {
            "net_lots": net_lots,
            "avg_buy_price": avg_buy_price
        }

    return result
