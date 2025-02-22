import bettingbot.selenium_utilities as _selenium
import bettingbot.sportmarket.sm_utilities as sm
from entity.bet.bet import Bet
from entity.pick.pick import Pick
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
        self.driver.get(bet.User.Url)
        # iniciar sesión
        sm.login(self.driver, bet.User.Username, bet.User.Password)
        # buscar el evento
        # TODO: comprobar antes si ya está en favs
        sm.set_favourite_event(self.driver, bet.Pick.Event)
        # comprobar la cuota y apostar si procede
        if sm.check_odds(self.driver, bet.Pick.Event, bet.Pick.MinOdds,
                         bet.Pick.Bet):  # TODO: cuidado, no estoy seguro de que la cuota sea ese td
            sm.place_bet(self.driver, bet.Pick.Event, bet.Pick.Bet, bet.Stake)
        # TODO: obtener la cuota colocada, que está en la fila del evento en el panel Pedidos recientes, en la columna Precio

        # TODO: cerrar el panel de Pedidos recientes
        pass
        # TODO: tenemos que determinar si se ha colocado correctamente, e indicarlo en el campo correspondiente de Bet.
        # eliminar de favoritos (opcional)
        sm.remove_event_from_favourites(self.driver, bet.Pick.Event, True)  # si falla lo reintentamos
        time.sleep(1)
        quit()

    # TODO: se debe llamar place_bet y recibir una Bet para poner la cuota colocada
    def place_pick(self, user: User, pick: Pick, stake : float) -> None:
        self.driver.get(user.Url)
        # iniciar sesión
        sm.login(self.driver, user.Username, user.Password)
        # buscar el evento
        # TODO: comprobar antes si ya está en favs
        sm.set_favourite_event(self.driver, pick.Event)
        # comprobar la cuota y apostar si procede
        if sm.check_odds(self.driver, pick.Event, pick.MinOdds,
                         pick.Bet):  # TODO: cuidado, no estoy seguro de que la cuota sea ese td
            sm.place_bet(self.driver, pick.Event, pick.Bet, stake)
        # TODO: obtener la cuota colocada, que está en la fila del evento en el panel Pedidos recientes, en la columna Precio

        # TODO: cerrar el panel de Pedidos recientes
        pass
        # eliminar de favoritos (opcional)
        sm.remove_event_from_favourites(self.driver, pick.Event, True)  # si falla lo reintentamos
        time.sleep(1)
        quit()
