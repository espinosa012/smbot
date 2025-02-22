from pymongo import MongoClient
from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database

from entity.bet import Bet
from entity.pick.pick import Pick

client : MongoClient = MongoClient("mongodb://localhost:27017/")

betsheet_db : Database = client["betsheet1"]
pick_coll : Collection = betsheet_db["pick"]

def insert_pick(pick : Pick) -> None:
    pick_coll.insert_one(pick.to_dict())

def insert_bet(bet : Bet) -> None:
    pick_coll.insert_one(bet.to_dict())