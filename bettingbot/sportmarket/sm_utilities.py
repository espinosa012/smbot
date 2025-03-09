import undetected_chromedriver as uc
from entity.bet.bet import Bet
from entity.pick.pick import Pick
from fuzz import fuzz_helper
import bettingbot.selenium_utilities as sel_util
import bettingbot.sportmarket.pageobject as pom

import random
import time

# TODO: loggers por todos lados

def login(driver: uc.Chrome, username: str, password: str) -> bool:
    try:
        sel_util.wait_element_clickable(driver, pom.LOGIN_BUTTON)
        sel_util.selenium_send_keys(driver, pom.LOGIN_USERNAME, username)
        sel_util.selenium_send_keys(driver, pom.LOGIN_PASSWORD, password)
        sel_util.selenium_click(driver, pom.LOGIN_BUTTON)
        time.sleep(random.uniform(0.5, 1))  # TODO: llevar esto y todos los que hay a selenium_utilities
        return sel_util.is_element_present(driver, pom.SEARCH_BUTTON, 20)
    except Exception as e:
        print(f"Error logging in: {e}")
        return False

# SEARCHING EVENT
def search_event(driver: uc.Chrome, pick : Pick) -> bool:  # true si lo encuentra, false si no
    open_search_modal(driver, True) # con 1 reintento
    ratio : float = search_event_in_search_modal_and_get_most_likely_ratio(driver, pick.Participants)
    minimum_ratio_for_searching_event: float = 70 # TODO a config
    if ratio < minimum_ratio_for_searching_event:
        return False
    click_best_search_result(driver, ratio, pick)
    return sel_util.is_element_present(driver, pom.FAVOURITES_SECTION_TBODY + pom.EVENT_ROW_TR)

def open_search_modal(driver: uc.Chrome, retry : bool) -> None:
    sel_util.wait_element_clickable(driver, pom.SEARCH_BUTTON, 20)
    time.sleep(random.uniform(1, 2))
    sel_util.selenium_click(driver, pom.SEARCH_BUTTON)
    sel_util.wait_element_visible(driver, pom.SEARCH_MODAL_DIV)
    search_modal = sel_util.find_element_by_xpath(driver, pom.SEARCH_MODAL_DIV)
    if retry and (not search_modal or not search_modal.is_displayed()):
        open_search_modal(driver, False)
    time.sleep(random.uniform(1.3, 2))

def search_event_in_search_modal_and_get_most_likely_ratio(driver: uc.Chrome, participants : list) -> float:
    # Deja la búsqueda hecha en el modal y devuelve el mejor ratio encontrado
    confidence_ration : float = 91  # TODO: a config
    event_max_ratio : float = get_search_result_most_likely_ratio(driver, str.join(" ", participants), participants) # calidad del mejor resultado obtenido introduciendo los dos
    if event_max_ratio >= confidence_ration: return event_max_ratio
    home_max_ratio : float = get_search_result_most_likely_ratio(driver, participants[0], participants)
    if home_max_ratio >= confidence_ration: return event_max_ratio
    away_max_ratio : float = get_search_result_most_likely_ratio(driver, participants[1], participants)  # calidad del mejor resultado obtenido introduciendo solo el away
    if away_max_ratio >= confidence_ration: return event_max_ratio

    # TODO: conversión QPR a Queens Park Rangers, Din. a Dinamo, etc (si no se encuentra)

    # Buscamos con qué string obtenemos el mejor resultado
    max_ratio : float = max(event_max_ratio, max(home_max_ratio, away_max_ratio))
    # TODO: es poco eficiente, calculamos el ratio 2 veces
    # comprobamos para cuál de las 3 strings hemos obtenido el mejor resultado e introducimos el término
    if max_ratio == away_max_ratio: search_term(driver, participants[1])
    elif max_ratio == home_max_ratio: search_term(driver, participants[0])
    elif max_ratio == event_max_ratio: search_term(driver, str.join(" ", participants))

    return max_ratio

def click_best_search_result(driver : uc.Chrome, likely_ratio : float, pick : Pick):
    # hacemos clic en la primera tarjeta cuya ratio coincida con el máximo
    best_search_result_xpath: str = get_search_result_xpath_by_ratio(driver, likely_ratio, pick.Participants)
    if best_search_result_xpath:
        set_pick_web_participant_names(driver, best_search_result_xpath, pick)
        sel_util.selenium_click(driver, best_search_result_xpath)
    time.sleep(random.uniform(0.5, 1.2))

def set_pick_web_participant_names(driver : uc.Chrome, best_search_result_xpath : str, pick : Pick):
    pick.WebParticipantNames = [p.strip() for p in (
        sel_util.find_element_by_xpath(driver, f"{best_search_result_xpath}{pom.SEARCH_RESULT_NAME}")
        .text.split(" vs. "))]  # tODO: separator a config

def get_search_result_xpath_by_ratio(driver : uc.Chrome, ratio : float, participants : list) -> str | None:
    sel_util.wait_element_clickable(driver, pom.SEARCH_RESULT_CARD)
    sel_util.random_wait(0.1, 0.3)
    for i in range(0, len(sel_util.find_elements_by_xpath(driver, pom.SEARCH_RESULT_CARD))):
        xpath: str = f"{pom.SEARCH_RESULT_CARD}[{i + 1}]{pom.SEARCH_RESULT_NAME}"
        search_result_event_string: str = sel_util.find_element_by_xpath(driver, xpath).text.lower()
        search_result_event_participants: list = [p.strip() for p in search_result_event_string.split(
            " vs. ")]  # TODO: a config el participants separator
        if ratio == compute_ratio(participants, search_result_event_participants):
            return f"{pom.SEARCH_RESULT_CARD}[{i + 1}]"
    return None

def search_term(driver : uc.Chrome, term : str) -> None:
    # TODO: al log
    click_all_sports_filter_in_search_modal(driver)
    sel_util.wait_element_visible(driver, pom.SEARCH_BAR_INPUT)
    sel_util.wait_element_clickable(driver, pom.SEARCH_BAR_INPUT)
    time.sleep(random.uniform(0.2, 0.45))
    if term == sel_util.find_element_by_xpath(driver, pom.SEARCH_BAR_INPUT).get_attribute("value").strip():
        return
    sel_util.selenium_clear_input(driver, pom.SEARCH_BAR_INPUT)
    sel_util.random_wait(0.1, 0.3)
    sel_util.selenium_send_keys(driver, pom.SEARCH_BAR_INPUT, term)

def click_all_sports_filter_in_search_modal(driver : uc.Chrome) -> None:
    # TODO: al logger
    if "selected" in sel_util.find_element_by_xpath(driver, f"{pom.SEARCH_MODAL_DIV}{pom.SEARCH_MODAL_ALL_SPORTS_FILTER}",
                                                    False, 3).get_attribute("class"):
        return
    sel_util.wait_element_visible(driver, f"{pom.SEARCH_MODAL_DIV}{pom.SEARCH_MODAL_ALL_SPORTS_FILTER}")
    sel_util.selenium_click(driver, f"{pom.SEARCH_MODAL_DIV}{pom.SEARCH_MODAL_ALL_SPORTS_FILTER}")
    sel_util.random_wait(1.3, 2.1)

def no_results_found(driver : uc.Chrome) -> bool:
    sel_util.random_wait(0.4, 0.9)
    return sel_util.is_element_present(driver, pom.NO_RESULTS_DIV, 2)

def get_found_event_cards(driver : uc.Chrome) -> list:
    sel_util.random_wait(0.4, 0.8)
    return sel_util.find_elements_by_xpath(driver, pom.SEARCH_RESULT_CARD, 3)

def get_search_result_most_likely_ratio(driver : uc.Chrome, searched_term : str, participants : list) -> float:
    """
    Devuelve el ratio mayor de entre todos los resultados de búsqueda que se muestran, en comparación con el término
    que recibe como argumento
    :param driver:
    :param searched_term:
    :param participants:
    :return:
    """
    max_ratio : float = 0
    search_term(driver, searched_term)
    if no_results_found(driver):
        return 0

    sel_util.wait_element_clickable(driver, pom.SEARCH_RESULT_CARD)
    sel_util.random_wait(0.1, 0.3)
    for i in range(0, len(sel_util.find_elements_by_xpath(driver, pom.SEARCH_RESULT_CARD))):
        xpath : str = f"{pom.SEARCH_RESULT_CARD}[{i+1}]{pom.SEARCH_RESULT_NAME}"
        search_result_event_string : str = sel_util.find_element_by_xpath(driver, xpath).text.lower()
        search_result_event_participants : list = [p.strip() for p in search_result_event_string.split(" vs. ")]    # TODO: a config el participants separator
        max_ratio = max(max_ratio, compute_ratio(participants, search_result_event_participants))
    return max_ratio

# TODO: llevar todos los cálculos del ratio fuera de aquí
def compute_ratio(pick_participants : list, search_result_event_participants : list) -> float:
    home_ratio: float = fuzz_helper.get_ratio(pick_participants[0].lower(), search_result_event_participants[0].lower())
    away_ratio: float = fuzz_helper.get_ratio(pick_participants[1].lower(), search_result_event_participants[1].lower())

    home_partial_ratio: float = fuzz_helper.get_partial_ratio(pick_participants[0].lower(), search_result_event_participants[0].lower())
    away_partial_ratio: float = fuzz_helper.get_partial_ratio(pick_participants[1].lower(), search_result_event_participants[1].lower())

    partial_ratio_factor : float = 0.65  # TODO: parametrizar
    computed_ratio: float  = ((1.0 - partial_ratio_factor) * (home_ratio + away_ratio)/2
                              + partial_ratio_factor * (home_partial_ratio + away_partial_ratio)/2)
    return min(100.0, computed_ratio)


# MARKETS
def place_bet(driver : uc.Chrome, bet : Bet):
    # clic en la cuota que corresponda
    try:
        click_selection(driver, bet.Pick.Participants, bet.Pick.Bet)
        # seleccionar la cuota
        click_best_odds(driver)
        # tomar valor de la cuota colocada
        bet.PlacedOdd = get_placed_odds(driver)
        # mandar stake y clic en apostar
        place_stake(driver, bet.Stake)
        # esperar que se muestre el modal de confirmación y clic
        confirm_bet_placing(driver)
        # cerrar el modal
        close_placer_modal(driver)
        return True
    except Exception as e:
        print(f"Error placing bet for user {bet.User.Username}: {e}")
        return False


def click_selection(driver : uc.Chrome, participants : list, bet : dict):
    selection_xpath : str = get_selection_xpath_by_event_and_bet(driver, participants, bet)
    sel_util.wait_element_clickable(driver, selection_xpath)
    sel_util.random_wait(0.8, 1.5)
    sel_util.selenium_click(driver, selection_xpath)

def click_best_odds(driver : uc.Chrome):
    sel_util.wait_element_visible(driver, pom.PLACER_MODAL_DIV)
    # TODO: me falta entenderlo bien, la cuota máxima puede estar limitada por el stake
    sel_util.selenium_click(driver, pom.PLACER_MODAL_DIV + pom.BEST_ODDS_SPAN)
    time.sleep(random.uniform(0.3, 0.6))

def get_placed_odds(driver : uc.Chrome):
    try:
        sel_util.wait_element_clickable(driver, pom.PLACED_ODDS_INPUT)
        sel_util.random_wait(0.1, 0.3)
        return float(sel_util.find_element_by_xpath(driver, pom.PLACED_ODDS_INPUT).get_attribute("value"))
    except Exception as e:
        print(f"Error getting placed odds: {e}")    # todo: al logger

def place_stake(driver : uc.Chrome, stake : float):
    sel_util.selenium_clear_input(driver, pom.STAKE_INPUT)
    time.sleep(random.uniform(0.3, 0.9))
    sel_util.selenium_send_keys(driver, pom.STAKE_INPUT, str(stake))
    time.sleep(random.uniform(0.7, 1))
    sel_util.selenium_click(driver, pom.PLACER_MODAL_DIV + pom.PLACE_BET_BUTTON)

def confirm_bet_placing(driver : uc.Chrome):
    sel_util.wait_element_visible(driver, pom.PLACE_CONFIRMATION_MODAL_DIV)
    time.sleep(random.uniform(0.3, 0.6))
    sel_util.selenium_click(driver, pom.PLACE_CONFIRMATION_MODAL_DIV + pom.PLACE_CONFIRMATION_MODAL_FOOTER_DIV
                            + pom.CONFIRM_PLACE_BUTTON)
    sel_util.wait_element_invisible(driver, pom.PLACE_CONFIRMATION_MODAL_DIV, 3)

def close_placer_modal(driver : uc.Chrome):
    try:    # no debe generar excepción
        sel_util.wait_element_clickable(driver, pom.PLACE_BET_BUTTON)
        sel_util.selenium_click(driver, pom.CLOSE_PLACER_MODAL_DIV)
        sel_util.wait_element_invisible(driver, pom.PLACER_MODAL_DIV)
    except Exception as e:
        print(f"Error closing placer modal: {e}")   # tODO: al logger, es leve

# ODDS
def check_odds(driver: uc.Chrome, participants: list, min_odds: float, bet: dict) -> bool:
    return get_odds(driver, participants, bet) >= min_odds

def get_odds(driver: uc.Chrome, participants: list, bet: dict) -> float:
    bet_web_element_xpath = get_selection_xpath_by_event_and_bet(driver, participants, bet)
    bet_web_element = sel_util.find_element_by_xpath(driver, bet_web_element_xpath)
    if bet_web_element:
        return float(bet_web_element.text)
    return 0    # TODO: informar por logger

def get_selection_xpath_by_event_and_bet(driver : uc.Chrome, participants : list, bet : dict) -> str | None:
    event_row_xpath: str = get_favourite_event_row_xpath(driver, participants)
    # event_row_xpath: str = pom.FAVOURITES_SECTION_TBODY + pom.EVENT_ROW_TR  # TODO: cuidado
    if bet["Market"] in ["1X2", "1x2"]:
        if bet["Selection"] == "H":
                return event_row_xpath + pom.EVENT_SELECTION_1X2_HOME_TD
        if bet["Selection"] == "D":
                return event_row_xpath + pom.EVENT_SELECTION_1X2_DRAW_TD
        if bet["Selection"] == "A":
                return event_row_xpath + pom.EVENT_SELECTION_1X2_AWAY_TD
    if bet["Market"] in ["TG"]:
        if "OVER" in bet["Selection"]:
            # TODO: check value
            return event_row_xpath + pom.EVENT_SELECTION_TOTAL_GOALS_OVER_TD
        if "UNDER" in bet["Selection"]:
            return event_row_xpath + pom.EVENT_SELECTION_TOTAL_GOALS_UNDER_TD
    if bet["Market"] in ["AH"]:
        if bet["Selection"] == "H":
                return event_row_xpath + pom.EVENT_SELECTION_AH_HOME_TD
        if bet["Selection"] == "A":
                return event_row_xpath + pom.EVENT_SELECTION_AH_AWAY_TD
    # TODO: enum de mercados y selections
    return ""

def get_favourite_event_row_xpath(driver : uc.Chrome, participants : list) -> str:
    event_row_xpath = pom.FAVOURITES_SECTION_TBODY + pom.EVENT_ROW_TR
    event_rows = sel_util.find_elements_by_xpath(driver, event_row_xpath)
    if event_rows:
        for elem in event_rows:
            if participants[0] in elem.text and participants[1] in elem.text:
                return f"{event_row_xpath}[{event_rows.index(elem) + 1}]"
    return ""   # TODO: generar excepción

def remove_event_from_favourites(driver : uc.Chrome, participants : list, retry : bool = False) -> None:
    try:
        sel_util.wait_element_clickable(driver, pom.FAVOURITE_EVENT_ICON, 5)
        sel_util.random_wait(0.85, 1.5)
        sel_util.selenium_click(driver, get_favourite_event_row_xpath(driver, participants) + pom.FAVOURITE_EVENT_ICON)
        sel_util.wait_element_invisible(driver, get_favourite_event_row_xpath(driver, participants))
        sel_util.wait_element_visible(driver, f"{pom.FAVOURITES_SECTION_TBODY}")
    except Exception as e:
        if retry:   remove_event_from_favourites(driver, participants, False)
        else: print(f"Error removing favourite event after retrying: {e}")

def close_footer(driver : uc.Chrome):
    # TODO: logger
    try:
        if not sel_util.is_element_present(driver, pom.EXPANDED_BET_BAR_FOOTER_DIV, 3):return
        sel_util.wait_element_clickable(driver, f"{pom.EXPANDED_BET_BAR_FOOTER_DIV}{pom.TOGGLE_BET_BAR_FOOTER_BUTTON}")
        sel_util.selenium_click(driver, f"{pom.EXPANDED_BET_BAR_FOOTER_DIV}{pom.TOGGLE_BET_BAR_FOOTER_BUTTON}")
        sel_util.random_wait(0.1, 0.4)
        sel_util.wait_element_invisible(driver, f"{pom.EXPANDED_BET_BAR_FOOTER_DIV}", 3)
        sel_util.random_wait(0.5, 0.8)
    except Exception as e:
        print(f"Exception closing footer> {e}") # TODO: al log