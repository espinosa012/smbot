import json

from flask import Flask, request

from bettingbot.sportmarket.SMBot import SMBot
from entity.pick import Pick

app = Flask(__name__)


@app.route('/')
def index():
    return '¡Hola, mundo!'


@app.route('/place-pick', methods=['POST'])
def place_pick():
    pick: Pick = Pick(json_pick=json.loads(request.data))
    bot = SMBot()
    pick.Stake = 1
    try:
        bot.place_bet(bot.users[1], pick)
    except Exception as e:
        print(e)
        bot.quit()
    bot.quit()
    return f"Placing pick:{pick}"


# TODO: orientar a objetos el servidor para lanzar fácilmente en paralelo el watcher del mail y el server

if __name__ == '__main__':
    app.run(debug=True)
