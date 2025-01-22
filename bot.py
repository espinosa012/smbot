import redis
from mail.mail_reader import MailReader
from bettingbot.selenium_utilities import get_driver
from bettingbot.sportmarket.SMBot import SMBot
from bettingbot.sportmarket import sm_utilities
from bettingbot.sportmarket.pageobject import *

if __name__ == "__main__":
    
    # bot = SMBot()
        # pruebas
    # bot.place_bet(bot.users[0], None)
    
    # input()
        
    reader = MailReader()
    reader.connect()
    reader.watch_inbox()