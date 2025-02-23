import bettingbot.selenium_utilities as _selenium
import bettingbot.sportmarket.sm_utilities as betinasia # TODO: cambiar nombre del módulo a betinasia
from entity.bet.bet import Bet
from entity.pick.pick import Pick
import time

from entity.user import User


class SMBot:
    config = {}
    driver = None

    def __init__(self, start_driver : bool = True):
        self.setup(start_driver)

    def setup(self, start_driver : bool):
        if start_driver:
            self.load_driver()

    # Config
    def load_driver(self):
        self.driver = _selenium.get_driver()

    def get_driver(self):
        if not self.driver:
            self.load_driver()
        return self.driver

    def quit(self):
        self.driver.close()

    # SportMarket/Betinasia black
    def place_bet(self, bet: Bet) -> bool:
        # TODO: es importante gestionar las excepciones y afectar a los campos de Bet
        bet_placed_ok: bool = False
        try:
            self.get_driver().get(bet.User.Url)
            # iniciar sesión
            betinasia.login(self.driver, bet.User.Username, bet.User.Password)
            # cerrar el panel de Pedidos recientes
            betinasia.close_footer(self.driver)
            # buscar el evento
            event_found : bool = betinasia.search_event(self.driver, bet.Pick)
            if not event_found:
                # TODO: indicar en el logger que el evento no se ha encontrado y notificar de alguna manera.
                #  Es un evento crítico. También indicar en el campo de la apuesta
                print(f"Event not foud: {bet.Pick.Event}")
                bet.IsPlaced = False
                bet.PlacingError = "Event not found" # TODO: usar enum
                return False

            # comprobar la cuota y apostar si procede (será configurable por usuario)
            # if betinasia.check_odds(self.driver, bet.Pick.WebParticipantNames, bet.Pick.MinOdds,bet.Pick.Bet):  # TODO: cuidado, no estoy seguro de que la cuota sea ese td

            bet_placed_ok = betinasia.place_bet(self.driver, bet)
            bet.IsPlaced = bet_placed_ok

            betinasia.remove_event_from_favourites(self.driver, bet.Pick.WebParticipantNames, True)  # si falla lo reintentamos

            time.sleep(1)
        except Exception as e:
            print(f"Error placing pick: {e}") # tODO: mejorar el mensaje y llevar a log
        return bet_placed_ok
