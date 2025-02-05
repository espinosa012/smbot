import os
import json
import bettingbot.selenium_utilities as _selenium
import bettingbot.sportmarket.sm_utilities as sm 
from pick.pick import Pick

class SMBot:

    config = {}
    driver = None
    users = []

    def __init__(self):
        self.setup()

    def setup(self):
        self.load_config()
        self.load_users()
        self.load_driver()

    # Config
    def load_config(self):
        self.config = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../config/params.json'), 'r'))
    
    def load_users(self):
        self.users = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../config/users.json'), 'r'))["sportmarket"]

    def load_driver(self):
        self.driver = _selenium.get_driver()
        self.driver.get(self.config["sportmarket_url"])
        # self.driver.get("https://deviceandbrowserinfo.com/info_device")


    # SportMarket
    def place_bet(self, user : dict, pick : Pick) -> None:
        # iniciar sesión
        sm.login(self.driver, user["username"], user["password"])
        # buscar el evento
        sm.search_event(self.driver, "Betis ")
        input()

        # comprobar la cuota y apostar si procede
        pass

