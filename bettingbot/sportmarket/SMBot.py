import time

import bettingbot.selenium_utilities as _selenium
import bettingbot.sportmarket.sm_utilities as betinasia
from entity.bet.bet import Bet


class SMBot:
    config = {}
    driver = None

    def __init__(self, is_headless : bool = True):
        self.setup(is_headless)

    def setup(self, is_headless : bool):
        self.load_driver(is_headless)

    # Config
    def load_driver(self, is_headless : bool):
        self.driver = _selenium.get_driver(is_headless)

    def get_driver(self):
        if not self.driver:
            self.load_driver()
        return self.driver

    def quit(self):
        self.driver.quit()

    def save_screenshot(self, path : str):
        # TODO
        self.driver.save_screenshot(path)

    # SportMarket/Betinasia black
    def place_bet(self, bet: Bet, check_min_odds : bool = False) -> bool:
        # TODO: es importante gestionar las excepciones y afectar a los campos de Bet
        try:
            self.get_driver().get(bet.User.Url)
            # iniciar sesión
            if not betinasia.login(self.driver, bet.User.Username, bet.User.Password):  # tODO: pasarle un parámetro retry
                print(f"Error logging in for user: {bet.User.Username} ({bet.User.Url}) [{bet.Pick.Event} - {bet.Pick.Bet['Selection']}]")   # TODO: logger
                bet.IsPlaced = False
                bet.PlacingError = "Error logging in"  # TODO: usar enum
                return False

            # cerrar el panel de Pedidos recientes
            betinasia.close_footer(self.driver)
            # buscar el evento
            event_found : bool = betinasia.search_event(self.driver, bet.Pick)
            # TODO: error searching event
            if not event_found:
                print(f"Event not found: {bet.Pick.Event} ({bet.Pick.Bet['Selection']})") # TODO: logger
                bet.IsPlaced = False
                bet.PlacingError = "Event not found" # TODO: usar enum
                return False

            # comprobar la cuota y apostar si procede (será configurable por usuario)
            # TODO: las cuotas de los asiáticos se miran de otra forma. Hay que cambiar la manera. Podríamos comprobarlo dentro del modal de colocación
            if check_min_odds and not betinasia.check_odds(self.driver, bet.Pick.WebParticipantNames,
                                                           bet.Pick.MinOdds,bet.Pick.Bet):
                print(f"Odds above minimum: {bet.Pick.Event}")
                bet.IsPlaced = False
                bet.PlacingError = "Odds above minimum"  # TODO: usar enum
                return False

            # TODO: error placing pick
            bet_placed_ok : bool = betinasia.place_bet(self.driver, bet)
            bet.IsPlaced = bet_placed_ok

            betinasia.remove_event_from_favourites(self.driver, bet.Pick.WebParticipantNames, True)  # si falla lo reintentamos
            time.sleep(1)
            return True

        except Exception as e:
            print(f"Exception placing pick {bet.Pick.Event} ({bet.Pick.Bet['Market']} - {bet.Pick.Bet['Selection']}): {e}")
            bet.IsPlaced = False
            bet.PlacingError = "Error placing bet"  # TODO: usar enum
            return False
