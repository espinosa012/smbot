from bettingbot.sportmarket.SMBot import SMBot
from mail.mail_reader import MailReader

if __name__ == "__main__":
    
    # bot = SMBot()
    # # pruebas
    # pick : Pick = Pick()
    # pick.Event = "Girona FC - Getafe"
    # pick.Bet = {"market": "AH", "selection":"H"}
    # pick.MinOdds = 1.6
    # pick.Stake = 1
    #
    # bot.place_bet(bot.users[1], pick)
    reader = MailReader()
    reader.connect()
    reader.watch()