import json
import os
import pickle
import threading

from flask import Flask, request

from bettingbot.sportmarket.SMBot import SMBot
from entity.bet.bet import Bet
from entity.pick.pick import Pick
from entity.user.user import User
from mail.mail_reader import MailReader

app: Flask = Flask(__name__)
mail_reader: MailReader = MailReader()


# TODO: lista de tareas:
#  1. leer el correo cada x tiempo con schedule, iniciando sesión cada vez, para que no caduque la sesión
#  2. Cuando una apuesta falle, notificar, almacenar en base de datos e implementar un método ágil para reintentar
#  3. Repasar bien todo el tema de base de datos (config, tablas, qué guardamos...)
#  4. En sm utilities, elevar excepciones con información para saber en qué punto del pipeline de colocación se ha producido el error

@app.route('/')
def index():
    return 'BetSheet Home'

@app.route('/watch', methods=['GET'])
def watch():
    print("Watching inbox...")
    threading.Thread(target=mail_reader.schedule_watching, args=([5])).start()
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
    for user in [u for u in get_config_users() if u.IsActive]:
        bet: Bet = Bet(pick, user, user.DefaultStake)
        print("------------------------------------------------")
        print(f"Placing bet for user {user.Username}")  # TODO: al logger
        bot : SMBot = SMBot(False)
        bot.place_bet(bet)  # TODO: gestionar excepción aquí
        bot.quit()
        # db.insert_bet(bet)    #TODO probar

def get_request_pick(req) -> Pick:
    return Pick(pick_dict=json.loads(req.data))

def get_config_users():
    users: list = []
    for user_dict in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config/users.json'),
                                    'r'))["betinasia"]:
        users.append(User(user_dict["url"], user_dict["username"], user_dict["password"], user_dict["default_stake"],
                          user_dict["active"]))
    return users


if __name__ == '__main__':
    # TODO: tomar de config
    host : str = "0.0.0.0"
    port : int = 5000

    app.run(host=host, port=port, debug=False)
