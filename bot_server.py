import json
import os
import pickle
import threading

from flask import Flask, request, redirect

from bettingbot.sportmarket.SMBot import SMBot
from entity.bet.bet import Bet
from entity.pick.pick import Pick
from entity.user import User
import db.mongo_helper as db
from mail.mail_reader import MailReader

app : Flask = Flask(__name__)
mail_reader : MailReader = MailReader()


@app.route('/')
def index():
    return 'BetSheet Home'

@app.route('/watch', methods=['GET'])
def watch():
    mail_reader.connect()
    print("Mail reader connected.")  # TODO: al logger
    if not mail_reader.IsWatching:
        print("Watching inbox...")  # TODO: al logger
        threading.Thread(target=mail_reader.watch, args=([True])).start()
    return "ok"

@app.route('/run-bot', methods=['GET'])
def run_bot():
    # TODO: arrancamos una instancia del SMBot
    pass

@app.route('/log', methods=['POST'])
def log():
    # TODO: usar un logger propio
    message : str = pickle.loads(request.data)
    return str(message)

@app.route('/logs', methods=['GET'])
def logs():
    # TODO: para mostrar los mensajes de logs
    pass

@app.route('/process-pick', methods=['POST'])
def process_pick():
    pick : Pick = get_request_pick(request)
    # TODO: lo guardamos en la base de datos o lo que sea que tengamos
    db.insert_pick(pick)
    # TODO: notificamos la llegada de un nuevo pick
    pass
    # TODO: para cada usuario activo, enviamos una peticion a place_bet.
    # comprobar si se puede lanzar en paralelo
    # for user in db.get_active_users():
    for user in get_config_users():
        bet : Bet = Bet(pick, user, 2)
        # TODO: colocamos la apuesta para el usuario, y cuando termine, el siguiente usuario
        print("Placing bet...") # TODO: al logger
        SMBot().place_bet(bet)
        # db.insert_bet(bet)    #TODO probar

    return "ok"

# TODO: cambiar nombre del endpoint
@app.route('/place-pick', methods=['POST'])
def place_pick():
    pick: Pick = get_request_pick(request)
    bot = SMBot()
    stake = 2
    users = get_config_users()
    juamvu = users[0]
    espinosa024 = users[1]

    print(f"Placing pick:{pick}")
    try:
        test_user = espinosa024
        bot.place_pick(test_user, pick, stake)
    except Exception as e:
        print(e)
    return f"Placing pick:{pick}"


# TODO: necesitamos un endpoint que reciba un pick y un usuario (o una Bet) y lo coloque. Así, quizás podamos
#  paralelizar la colocación del pick, con un hilo para cada usuario
def get_request_pick(req) -> Pick:
    return Pick(pick_dict=json.loads(req.data))

def get_config_users():
    users: list = []
    for user_dict in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config/config.json'),
                                    'r'))["users"]["betinasia"]:
        users.append(User(user_dict["url"], user_dict["username"], user_dict["password"], user_dict["active"]))
    return users




if __name__ == '__main__':
    app.run(debug=True)
