import undetected_chromedriver as uc

import bettingbot.pagui.pyautogui_utilities as pagui
import bettingbot.selenium_utilities as sel_util
import bettingbot.sportmarket.pageobject as pom

def login(driver: uc.Chrome, username: str, password: str) -> None:
    sel_util.wait_element_clickable(driver, pom.LOGIN_BUTTON)
    sel_util.selenium_send_keys(driver, pom.LOGIN_USERNAME, username)
    sel_util.selenium_send_keys(driver, pom.LOGIN_PASSWORD, password)
    sel_util.selenium_click(driver, pom.LOGIN_BUTTON)
    sel_util.wait_element_clickable(driver, pom.SEARCH_BUTTON, 20)
    pagui.random_wait(0.5, 1)

# SEARCHING EVENT
def search_event(driver: uc.Chrome, event: str) -> bool:  # true si lo encuentra, false si no
    open_search_modal(driver, True) # con 1 reintento
    search_event_in_search_modal(driver, event)
    return sel_util.is_element_present(driver, pom.FAVOURITES_SECTION_TBODY + pom.EVENT_ROW_TR)

def open_search_modal(driver: uc.Chrome, retry : bool) -> None:
    sel_util.wait_element_clickable(driver, pom.SEARCH_BUTTON, 20)
    pagui.random_wait(1, 2)
    sel_util.selenium_click(driver, pom.SEARCH_BUTTON)
    sel_util.wait_element_visible(driver, pom.SEARCH_MODAL_DIV)
    search_modal = sel_util.find_element_by_xpath(driver, pom.SEARCH_MODAL_DIV)
    if retry and (not search_modal or not search_modal.is_displayed()):
        open_search_modal(driver, False)
    pagui.random_wait(1.3, 2)

def search_event_in_search_modal(driver: uc.Chrome, event: str) -> None:
    sel_util.wait_element_visible(driver, pom.SEARCH_BAR_INPUT)
    sel_util.wait_element_clickable(driver, pom.SEARCH_BAR_INPUT)
    pagui.random_wait(0.2, 0.45)
    sel_util.selenium_send_keys(driver, pom.SEARCH_BAR_INPUT, event)
    pagui.random_wait(0.8, 1.2)
    # click en la tarjeta con el resultado deseado
    select_search_result(driver, event)
    pagui.random_wait(0.5, 1.2)

def select_search_result(driver: uc.Chrome, event: str) -> None:
    # TODO: se puede mejorar. No hacer clic en la primera tarjeta, buscar la tarjeta según el contenido del string event
    sel_util.selenium_click(driver, pom.SEARCH_RESULT_CARD)
    pagui.random_wait(0.4, 0.7)
    # esperamos que se oculte el modal y una cantidad aleatoria de tiempo, o que sea clickable el botón de la cuota
    sel_util.wait_element_invisible(driver, pom.SEARCH_MODAL_DIV, 3)


# MARKETS
def place_bet(driver : uc.Chrome, event : str, bet : dict, stake : float):
    # clic en la cuota que corresponda
    click_selection(driver, event, bet)
    # seleccionar la cuota
    click_best_odds(driver)
    # mandar stake y clic en apostar
    place_stake(driver, stake)
    # esperar que se muestre el modal de confirmación y click
    confirm_bet_placing(driver)
    # cerrar el modal
    close_placer_modal(driver)

# TODO: usar get_selection_webelement_by_event_and_bet
def click_selection(driver : uc.Chrome, event : str, bet : dict):
    sel_util.selenium_click(driver, get_selection_xpath_by_event_and_bet(driver, event, bet))

def click_best_odds(driver : uc.Chrome):
    sel_util.wait_element_visible(driver, pom.PLACER_MODAL_DIV)
    # TODO: me falta entenderlo bien, la cuota máxima puede estar limitada por el stake
    sel_util.selenium_click(driver, pom.PLACER_MODAL_DIV + pom.BEST_ODDS_SPAN)
    pagui.random_wait(0.3, 0.6)

def place_stake(driver : uc.Chrome, stake : float):
    sel_util.selenium_clear_input(driver, pom.STAKE_INPUT)
    pagui.random_wait(0.3, 0.9)
    sel_util.selenium_send_keys(driver, pom.STAKE_INPUT, str(stake))
    pagui.random_wait(0.7, 1)
    sel_util.selenium_click(driver, pom.PLACER_MODAL_DIV + pom.PLACE_BET_BUTTON)

def confirm_bet_placing(driver : uc.Chrome):
    sel_util.wait_element_visible(driver, pom.PLACE_CONFIRMATION_MODAL_DIV)
    pagui.random_wait(0.3, 0.6)
    sel_util.selenium_click(driver, pom.PLACE_CONFIRMATION_MODAL_DIV + pom.PLACE_CONFIRMATION_MODAL_FOOTER_DIV
                            + pom.CONFIRM_PLACE_BUTTON)
    sel_util.wait_element_invisible(driver, pom.PLACE_CONFIRMATION_MODAL_DIV)

def close_placer_modal(driver : uc.Chrome):
    sel_util.wait_element_clickable(driver, pom.PLACE_BET_BUTTON)
    sel_util.selenium_click(driver, pom.CLOSE_PLACER_MODAL_DIV)
    sel_util.wait_element_invisible(driver, pom.PLACER_MODAL_DIV)

# ODDS
def check_odds(driver: uc.Chrome, event: str, min_odds: float, bet: dict) -> bool:
    return get_odds(driver, event, bet) >= min_odds

def get_odds(driver: uc.Chrome, event: str, bet: dict) -> float:
    bet_web_element_xpath = get_selection_xpath_by_event_and_bet(driver, event, bet)
    bet_web_element = sel_util.find_element_by_xpath(driver, bet_web_element_xpath)
    if bet_web_element:
        return float(bet_web_element.text)
    return 0    # tODO: informar por logger

def get_selection_xpath_by_event_and_bet(driver : uc.Chrome, event : str, bet : dict) -> str | None:
    event_row_xpath: str = get_favourite_event_row_xpath(driver, event)
    if bet["market"] in ["1X2", "1x2"]:
        if bet["selection"] == "H":
                return event_row_xpath + pom.EVENT_SELECTION_1X2_HOME_TD
        if bet["selection"] == "D":
                return event_row_xpath + pom.EVENT_SELECTION_1X2_DRAW_TD
        if bet["selection"] == "A":
                return event_row_xpath + pom.EVENT_SELECTION_1X2_AWAY_TD
    if bet["market"] in ["TG", "Total Goals", "Total goals"]:
        if bet["selection"] == "OVER":
            return event_row_xpath + pom.EVENT_SELECTION_TOTAL_GOALS_OVER_TD
        if bet["selection"] == "UNDER":
            return event_row_xpath + pom.EVENT_SELECTION_TOTAL_GOALS_UNDER_TD
    if bet["market"] in ["AH", "Asian Handicap"]:
        if bet["selection"] == "H":
                return event_row_xpath + pom.EVENT_SELECTION_AH_HOME_TD
        if bet["selection"] == "A":
                return event_row_xpath + pom.EVENT_SELECTION_AH_AWAY_TD
    return ""

def get_favourite_event_row_xpath(driver : uc.Chrome, event : str) -> str:
    participants : list = event.split(" - ")    # TODO: depende del formato del string del event
    event_row_xpath = pom.FAVOURITES_SECTION_TBODY + pom.EVENT_ROW_TR
    event_rows = sel_util.find_elements_by_xpath(driver, event_row_xpath)
    if event_rows:
        for elem in event_rows:
            if participants[0] in elem.text and participants[1] in elem.text:
                return f"{event_row_xpath}[{event_rows.index(elem) + 1}]"
    return ""   # TODO: generar excepcion

def remove_event_from_favourites(driver : uc.Chrome, event : str) -> None:
    sel_util.selenium_click(driver, get_favourite_event_row_xpath(driver, event) + pom.FAVOURITE_EVENT_ICON)
    sel_util.wait_element_invisible(driver, get_favourite_event_row_xpath(driver, event))
