from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth, rojadirecta
import math
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/audit",
    tags=["audit"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/games")
def get_inventory():

    with db.engine.begin() as connection:
        games = connection.execute(sqlalchemy.text("SELECT * FROM games")).fetchall()
    
    print(games)
    
    return {"games": 123}



@router.post("/games")
def post_audit_results():
    
    games = rojadirecta.get_games()

    print(games)
    
    with db.engine.begin() as connection:
        for i in games:
            games = connection.execute(sqlalchemy.text("INSERT INTO games (sport, league, team1, team2, matchtime, link) VALUES (:sport, :league, :team1, :team2, :matchtime, :link)"), {
                                                    'sport': i[0],
                                                    'league': i[1],
                                                    'team1': i[2],
                                                    'team2': i[3],
                                                    'matchtime': i[4],
                                                    'link': i[5]
                                                })

    return "OK"
