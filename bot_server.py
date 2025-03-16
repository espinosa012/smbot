import json
import os
import pickle
import threading

import requests
from flask import Flask, request

from bettingbot.sportmarket.SMBot import SMBot
from entity.bet.bet import Bet
from entity.pick.pick import Pick
from entity.user import User
from mail.mail_reader import MailReader

app: Flask = Flask(__name__)
mail_reader: MailReader = MailReader()


@app.route('/')
def index():
    return 'BetSheet Home'


@app.route('/watch', methods=['GET'])
def watch():
    # TODO: cambiar. nos conectamos cada x tiempo (periodo largo) y comprobamos los mensajes nuevos
    mail_reader.connect()
    print("Mail reader connected.")  # TODO: al logger
    if not mail_reader.IsWatching:
        print("Watching inbox...")  # TODO: al logger
        threading.Thread(target=mail_reader.watch, args=([True])).start()
    return "ok"


@app.route('/stop-watching', methods=['GET'])
def stop_watching():
    print("Mail reader stopped watching.")  # TODO: al logger
    mail_reader.stop_watching()
    return "ok"


@app.route('/log', methods=['POST'])
def log():
    # TODO: usar un logger propio
    message: str = pickle.loads(request.data)
    return str(message)


@app.route('/logs', methods=['GET'])
def logs():
    # TODO: para mostrar los mensajes de logs
    pass


@app.route('/process-pick', methods=['POST'])
def process_pick():
    pick: Pick = get_request_pick(request)
    # almacenamos el pick en la base de datos
    # db.insert_pick(pick)
    # TODO: notificamos la llegada de un nuevo pick
    pass
    # Colocamos el pick secuencialmente para cada usuario
    place_pick(pick)
    return "ok"


def schedule_pick(pick: Pick):
    # TODO: En función de la estrategia, se planifica la colocación para una determinada hora.
    # para todas las estrategias excepto Ready03, colocamos el pick unos 35 o 40 minutos antes del evento (mirando date y time del pick).
    # si ha pasado ese tiempo, la colocamos inmediatamente (es decir, se planifica para dentro de unos segundos)
    pass


def place_pick(pick: Pick):
    # TODO: si se produce error en la colocación, deberíamos devolver False
    # for user in db.get_active_users():
    # for user in [get_config_users()[1]]:
    for user in [u for u in get_config_users() if u.IsActive]:
        bet: Bet = Bet(pick, user, user.DefaultStake)
        print(f"Placing bet for user {user.Username}")  # TODO: al logger
        bot = SMBot()
        bot.place_bet(bet)  # TODO: gestionar excepción aquí
        bot.quit()
        print("------------------------------------------------")
        # db.insert_bet(bet)    #TODO probar

def get_request_pick(req) -> Pick:
    return Pick(pick_dict=json.loads(req.data))

def get_config_users():
    users: list = []
    for user_dict in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config/config.json'),
                                    'r'))["users"]["betinasia"]:
        users.append(User(user_dict["url"], user_dict["username"], user_dict["password"], user_dict["default_stake"],
                          user_dict["active"]))
    return users


def start_watching(_host : str, _port : int):
    print(f"http://{_host}:{_port}/watch")
    requests.get(f"http://{_host}:{_port}/watch", headers={'Content-Type': 'application/json'})

# TODO: parámetros de lanzamiento: headless, procesar mensajes previos de la bandeja de entrada


if __name__ == '__main__':
    host : str = "127.0.0.1"
    port : int = 5000

    # threading.Thread(target=app.run).start()
    # time.sleep(5)
    # threading.Thread(target=start_watching, args=([host, port])).start()
    app.run(host=host, port=port, debug=False)
