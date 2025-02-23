import undetected_chromedriver as uc
from undetected_chromedriver import WebElement

from fuzz import fuzz_helper
import bettingbot.selenium_utilities as sel_util
import bettingbot.sportmarket.pageobject as pom

import random
import time

# TODO: loggers por todos lados

def login(driver: uc.Chrome, username: str, password: str) -> None:
    sel_util.wait_element_clickable(driver, pom.LOGIN_BUTTON)
    sel_util.selenium_send_keys(driver, pom.LOGIN_USERNAME, username)
    sel_util.selenium_send_keys(driver, pom.LOGIN_PASSWORD, password)
    sel_util.selenium_click(driver, pom.LOGIN_BUTTON)
    sel_util.wait_element_clickable(driver, pom.SEARCH_BUTTON, 20)
    time.sleep(random.uniform(0.5, 1))  # TODO: llevar esto y todos los que hay a selenium_utilities

# SEARCHING EVENT
def search_event(driver: uc.Chrome, participants : list) -> bool:  # true si lo encuentra, false si no
    open_search_modal(driver, True) # con 1 reintento
    ratio : float = search_event_in_search_modal_and_get_most_likely_ratio(driver, participants)
    minimum_ratio_for_searching_event: float = 61 # TODO a config
    if ratio < minimum_ratio_for_searching_event:
        return False    # TODO: y ponemos en Bet el error EVENT_NOT_FOUND
    click_best_search_result(driver, ratio, participants)
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
    event_max_ratio : float = get_search_result_most_likely_ratio(driver, str.join(" ", participants), participants) # calidad del mejor resultado obtenido introduciendo los dos
    home_max_ratio : float = get_search_result_most_likely_ratio(driver, participants[0], participants)
    away_max_ratio : float = get_search_result_most_likely_ratio(driver, participants[1], participants)  # calidad del mejor resultado obtenido introduciendo solo el away
    # TODO: podríamos decir que si alguno es superior a un umbral grande, tipo 90, damos por hecho que es el mejor
    # Buscamos con qué string obtenemos el mejor resultado
    max_ratio : float = max(event_max_ratio, max(home_max_ratio, away_max_ratio))
    # TODO: es poco eficiente, calculamos el ratio 2 veces
    # comprobamos para cuál de las 3 strings hemos obtenido el mejor resultado e introducimos el término
    if max_ratio == event_max_ratio: search_term(driver, str.join(" ", participants))
    elif max_ratio == away_max_ratio: search_term(driver, participants[1])
    elif max_ratio == home_max_ratio: search_term(driver, participants[0])

    return max_ratio

def click_best_search_result(driver : uc.Chrome, likely_ratio : float, participants : list):
    # hacemos clic en la primera tarjeta cuya ratio coincida con el máximo
    best_search_result_xpath: str = get_search_result_xpath_by_ratio(driver, likely_ratio, participants)
    if best_search_result_xpath:
        #   TODO: necesitamos devolver de alguna manera el nombre con el que aparecen los participants en la web para
        #    encontrar luego la fila en favs (variable global o algo)
        web_participants = [p.strip() for p in (
            sel_util.find_element_by_xpath(driver, f"{best_search_result_xpath}{pom.SEARCH_RESULT_NAME}")
            .text.split(" vs. "))]

        sel_util.selenium_click(driver, best_search_result_xpath)
    time.sleep(random.uniform(0.5, 1.2))

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

def get_most_likely_event_card_xpath(driver : uc.Chrome, participants : list) -> str:
    """
    Para obtener el resultado de búsqueda más parecido para el evento
    :param driver: 
    :param participants: 
    :return: 
    """
    # TODO: obtenemos el ratio fuzz para cada tarjeta y devolvemos la más similar si supera cierto umbral, en caso contrario, None
    most_likely_card_xpath : str = ""
    for card in get_found_event_cards(driver):
        pass
    return most_likely_card_xpath

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

def click_selection(driver : uc.Chrome, event : str, bet : dict):
    sel_util.selenium_click(driver, get_selection_xpath_by_event_and_bet(driver, event, bet))

def click_best_odds(driver : uc.Chrome):
    sel_util.wait_element_visible(driver, pom.PLACER_MODAL_DIV)
    # TODO: me falta entenderlo bien, la cuota máxima puede estar limitada por el stake
    sel_util.selenium_click(driver, pom.PLACER_MODAL_DIV + pom.BEST_ODDS_SPAN)
    time.sleep(random.uniform(0.3, 0.6))

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
    return 0    # TODO: informar por logger

def get_selection_xpath_by_event_and_bet(driver : uc.Chrome, event : str, bet : dict) -> str | None:
    # event_row_xpath: str = get_favourite_event_row_xpath(driver, event)
    event_row_xpath: str = pom.FAVOURITES_SECTION_TBODY + pom.EVENT_ROW_TR  # TODO: cuidado
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

def get_favourite_event_row_xpath(driver : uc.Chrome, event : str) -> str:
    participants : list = event.split(" - ")    # TODO: depende del formato del string del event
    event_row_xpath = pom.FAVOURITES_SECTION_TBODY + pom.EVENT_ROW_TR
    event_rows = sel_util.find_elements_by_xpath(driver, event_row_xpath)
    if event_rows:
        for elem in event_rows:
            if participants[0] in elem.text and participants[1] in elem.text:
                return f"{event_row_xpath}[{event_rows.index(elem) + 1}]"
    return ""   # TODO: generar excepcion

def remove_event_from_favourites(driver : uc.Chrome, event : str, retry : bool = False) -> None:
    try:
        sel_util.selenium_click(driver, get_favourite_event_row_xpath(driver, event) + pom.FAVOURITE_EVENT_ICON)
        sel_util.wait_element_invisible(driver, get_favourite_event_row_xpath(driver, event))
    except Exception as e:
        if retry:   remove_event_from_favourites(driver, event, False)
        else: print(f"Error removing favourite event after retrying: {e}")

