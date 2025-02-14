import os
import json
import time

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
        self.users = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../config/users.json'),
                                    'r'))["sportmarket"]

    def load_driver(self):
        self.driver = _selenium.get_driver()

    # SportMarket/Betinasia black
    def place_bet(self, user : dict, pick : Pick) -> None:
        self.driver.get(user["url"])
        # iniciar sesión
        sm.login(self.driver, user["username"], user["password"])
        # buscar el evento
        # TODO: comprobar antes si ya está en favs
        sm.search_event(self.driver, pick.Event)
        # comprobar la cuota y apostar si procede
        if sm.check_odds(self.driver, pick.Event, pick.MinOdds, pick.Bet):  # TODO: cuidado, no estoy seguro de que la cuota sea ese td
            sm.place_bet(self.driver, pick.Event, pick.Bet, pick.Stake)
        # eliminar de favoritos (opcional)
        sm.remove_event_from_favourites(self.driver, pick.Event)
        time.sleep(10)
