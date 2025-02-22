import json
import os
import pickle

from flask import Flask, request, redirect

from bettingbot.sportmarket.SMBot import SMBot
from entity.pick.pick import Pick
from entity.user import User

app = Flask(__name__)


@app.route('/')
def index():
    return 'BetSheet Home'

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
    # TODO: lo guardamos en la base de datos o lo que sea que tengamos
    get_request_pick(request).save_to_csv()
    # print(json.loads(request.data))
    # TODO: notificamos la llegada de un nuevo pick
    pass
    # Lo enviamos al endpoint correspondiente para la colocación
    # redirect("/place-bet")
    return "ok"

@app.route('/place-bet', methods=['POST'])
def place_bet():
    bet = json.loads(request.data)
    return str(bet)

# TODO: cambiar nombre del endpoint
@app.route('/place-pick', methods=['POST'])
def place_pick():
    pick: Pick = get_request_pick()
    bot = SMBot()
    pick.Stake = 2
    users = get_config_users()
    juamvu = users[0]
    espinosa024 = users[1]
    print(f"Placing pick:{pick}")
    try:
        test_user = espinosa024
        bot.place_pick(test_user, pick)
    except Exception as e:
        print(e)
        bot.quit()
    bot.quit()
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
