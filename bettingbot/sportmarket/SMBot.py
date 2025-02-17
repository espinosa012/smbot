import bettingbot.selenium_utilities as _selenium
import bettingbot.sportmarket.sm_utilities as sm
from entity.bet import Bet
from entity.pick import Pick
import time

from entity.user import User


class SMBot:
    config = {}
    driver = None

    def __init__(self):
        self.setup()

    def setup(self):
        self.load_driver()

    # Config
    def load_driver(self):
        self.driver = _selenium.get_driver()

    def quit(self):
        self.driver.close()

    # SportMarket/Betinasia black
    def place_bet(self, bet: Bet) -> None:
        # iniciamos sesión
        pass
        # recorremos los picks de la apuesta y los vamos colocando con place_pick
        pass
        # cerramos el navegador
        pass

    # TODO: usar nuestra entidad usuario (o usaurio Sportmarket)
    def place_pick(self, user: User, pick: Pick) -> None:
        self.driver.get(user.Url)
        # iniciar sesión
        sm.login(self.driver, user.Username, user.Password)
        # buscar el evento
        # TODO: comprobar antes si ya está en favs
        sm.set_favourite_event(self.driver, pick.Event)
        # comprobar la cuota y apostar si procede
        if sm.check_odds(self.driver, pick.Event, pick.MinOdds,
                         pick.Bet):  # TODO: cuidado, no estoy seguro de que la cuota sea ese td
            sm.place_bet(self.driver, pick.Event, pick.Bet, pick.Stake)
        # eliminar de favoritos (opcional)
        sm.remove_event_from_favourites(self.driver, pick.Event, True)  # si falla lo reintentamos
        time.sleep(1.5)
