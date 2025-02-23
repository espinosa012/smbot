from bettingbot.sportmarket.SMBot import SMBot
from entity.bet.bet import Bet
from entity.pick.pick import Pick
from entity.user import User


def get_config_users():
    users: list = []
    import json
    import os
    for user_dict in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config/config.json'),
                                    'r'))["users"]["betinasia"]:
        users.append(User(user_dict["url"], user_dict["username"], user_dict["password"], user_dict["active"]))
    return users


# print(fuzz_helper.get_ratio("Maastricht Den Haag", "MVV Maastricht ADO Den Haag"))
# print(fuzz_helper.get_ratio("LASK SK Rapid", "LASK SK Rapid Wien"))
# print(fuzz_helper.get_ratio("Portland Timbers Vancouver Whitecaps", "Portland Timbers Vancouver Whitecaps FC"))
# print(fuzz_helper.get_partial_ratio("Watford Luton", "Watford Luton Town"))

bot = SMBot()
pick = Pick()
pick.Event = "Plaza Colonia - Defensor Sp."
pick.Participants  = ["Plaza Colonia", "Defensor Sp."]
pick.Bet = {"Market":"1X2", "Selection":"H"}
pick.MinOdds = 3.59
bot.place_bet(Bet(pick, get_config_users()[1], 1))



# if __name__ == "__main__":
#     reader = MailReader()
#     reader.connect()
#     reader.watch(process_previous_messages=True)