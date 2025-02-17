import json
import os

from flask import Flask, request

from bettingbot.sportmarket.SMBot import SMBot
from entity.pick import Pick
from entity.user import User

app = Flask(__name__)


@app.route('/')
def index():
    return '¡Hola, mundo!'

@app.route('/place-pick', methods=['POST'])
def place_bet():
    bet = json.loads(request.data)
    return str(bet)

# TODO: cambiar nombre del endpoint
@app.route('/place-pick', methods=['POST'])
def place_pick():
    pick: Pick = Pick(pick_dict=json.loads(request.data))
    bot = SMBot()
    pick.Stake = 1
    users = get_config_users()

    juamvu = users[0]
    espinosa024 = users[1]

    try:
        test_user = espinosa024
        bot.place_pick(test_user, pick)
    except Exception as e:
        print(e)
        bot.quit()
    bot.quit()
    return f"Placing pick:{pick}"


def get_config_users():
    users: list = []
    for user_dict in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config/config.json'),
                                    'r'))["users"]["betinasia"]:
        users.append(User(user_dict["url"], user_dict["username"], user_dict["password"], user_dict["active"]))
    return users




if __name__ == '__main__':
    app.run(debug=True)
