import json
import os

from bettingbot.sportmarket.SMBot import SMBot
from entity.bet.bet import Bet
from entity.pick.pick import Pick
from entity.user import User


def get_config_users():
    users: list = []
    for user_dict in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config/config.json'),
                                    'r'))["users"]["betinasia"]:
        users.append(User(user_dict["url"], user_dict["username"], user_dict["password"], user_dict["default_stake"], user_dict["active"]))
    return users


bot = SMBot()
pick = Pick()
pick.Event = "Real Sociedad - Real Madrid"
pick.Participants = ["Real Sociedad", "Real Madrid"]
pick.Bet = {"Market":"1X2", "Selection":"A"}
pick.MinOdds = 1.8
bot.place_bet(Bet(pick, get_config_users()[1], 1))
bot.quit()

# if __name__ == "__main__":
#     reader = MailReader()
#     reader.connect()
#     reader.watch(process_previous_messages=True)