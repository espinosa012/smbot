from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from pymongo.synchronous.collection import Collection
from pymongo.synchronous.database import Database

from entity.bet.bet import Bet
from entity.pick.pick import Pick

client : MongoClient = MongoClient("mongodb://localhost:27017/")    # TODO: llevar a config

betsheet_db : Database = client["betsheet1"]
pick_coll : Collection = betsheet_db["pick"]
bet_coll : Collection = betsheet_db["bet"]
user_coll : Collection = betsheet_db["user"]
config_coll : Collection = betsheet_db["config"]

# TODO: sustituir config por db y cambiar en todos lados

def find_by_kv(coll_name : str, key : str, value : any):
    pass

def insert_pick(pick : Pick) -> None:
    # TODO: consideramos que está duplicado si tiene la misma UID, evento y bet
    try:
        pick_coll.insert_one(pick.to_dict())
    except DuplicateKeyError:
        print(f"Clave duplicada ({pick.to_dict()["_id"]})")    # TODO: al logger

def insert_bet(bet : Bet) -> None:
    try:
        bet_coll.insert_one(bet.to_dict())
    except DuplicateKeyError:
        print(f"Clave duplicada ({bet.to_dict()["_id"]})")  # TODO: al logger

def get_active_users() -> list:
    active_users : list = []
    for u in user_coll.find({"active":True}):
        pass    # TODO: formamos el User a partir del documento
    return active_users
