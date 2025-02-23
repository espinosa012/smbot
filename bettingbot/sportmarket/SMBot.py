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
    def place_bet(self, bet: Bet) -> None:
        # TODO: es importante gestionar las excepciones y afectar a los campos de Bet
        try:
            self.get_driver().get(bet.User.Url)
            # iniciar sesión
            betinasia.login(self.driver, bet.User.Username, bet.User.Password)
            # TODO: cerrar el panel de Pedidos recientes
            betinasia.close_footer(self.driver)
            pass
            # buscar el evento
            betinasia.search_event(self.driver, bet.Pick)
            # TODO: si no lo hemos encontrado (ratio minimo), lo indicamos en la Bet e interrumpimos la colocación

            # comprobar la cuota y apostar si procede
            if betinasia.check_odds(self.driver, bet.Pick.WebParticipantNames, bet.Pick.MinOdds,
                                    bet.Pick.Bet):  # TODO: cuidado, no estoy seguro de que la cuota sea ese td
                betinasia.place_bet(self.driver, bet.Pick.WebParticipantNames, bet.Pick.Bet, bet.Stake)
            # TODO: obtener la cuota colocada, que está en la fila del evento en el panel Pedidos recientes, en la columna Precio


            # TODO: tenemos que determinar si se ha colocado correctamente, e indicarlo en el campo correspondiente de Bet.
            # eliminar de favoritos (opcional)
            betinasia.remove_event_from_favourites(self.driver, bet.Pick.WebParticipantNames, True)  # si falla lo reintentamos
            time.sleep(1)
        except Exception as e:
            print(f"Exception placing pick: {e}") # tODO: mejorar el mensaje y llevar a log
        time.sleep(2)
