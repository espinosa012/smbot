import bettingbot.selenium_utilities as sel_util
import bettingbot.sportmarket.pageobject as pom 
import undetected_chromedriver as uc
from pick.pick import Pick
import bettingbot.pagui.pyautogui_utilities as pagui
import time

def place_bet(pick : Pick, user) -> None:
    # TODO: método que se llama desde fuera para realizar el pipeline completo de la apuesta
    pass

def login(driver : uc.Chrome, username : str, password : str) -> None:
    sel_util.wait_element_clickable(driver, pom.LOGIN_BUTTON)
    sel_util.selenium_send_keys(driver, pom.LOGIN_USERNAME, username)
    sel_util.selenium_send_keys(driver, pom.LOGIN_PASSWORD, password)
    sel_util.selenium_click(driver, pom.LOGIN_BUTTON)
    sel_util.wait_element_clickable(driver, pom.SEARCH_BUTTON, 20)

    # hacer clic, con nuestro método para mover el ratón hasta la posición,  en un lugar aleatorio del cuadro de texto de usuario (offset aleatorio del centro o la posición que devuelva selenium)
    # usando nuestra manera con paradas aleatorias, introducir nombre de usuario
    # espera aleatoria de entorno a 0.7s antes de hacer clic en el input o pulsar tab de la contraseña, con el método para mover el ratón
    # repetir los pasos anteriores para la controseña
    # otra espeara aleatoria similar y clic en el botón de login (podríamos meter la espera en el propio método de click)
    # una alternativa al paso anterior sería pulsar 2 veces tab, ya que la primera vez pondrá el foco en el check de mostrar contraseña. luego, pulsar espacio para hacer click en el botón de login
    # esperar con selenium a que se muestre el home
    pass

def search_event(driver : uc.Chrome, event : str) -> bool:  # true si lo encuentra, false si no
    # ctrl + f para mostrar el modal
    sel_util.wait_element_clickable(driver, pom.SEARCH_BUTTON, 20)
    pagui.random_wait(1, 2)
    sel_util.selenium_click(driver, pom.SEARCH_BUTTON)
    # esperar que se muestre el modal de búsqueda
    pass
    pagui.random_wait(1, 2)
    # pagui.ctrlF()   # otra alternativa es hacer clic en el botón de la lupa
    pagui.random_wait(0.7, 0.9)
    input()
    sel_util.selenium_send_keys(driver, pom.SEARCH_BAR_INPUT, event)
    # click en la tarjeta con el resultado deseado
    # esperamos que se ocullte el modal y una cantidad aleatoria de tiempo, o que sea clickable el botón de la cuota

    # devolvemos true si hemos conseguido encontrar el evento y se muestra en los favoritos o donde corresponda
    return False

def select_search_result(driver : uc.Chrome, event : str) -> None:
    pass

def check_odds(driver : uc.Chrome, min_odds : float, selection) -> bool:
    return get_odds(driver, selection) >= min_odds

def get_odds(driver : uc.Chrome, selection) -> float: 
    # usando selenium
    return 0



# TODO: con ctrl+f aparece el cuadro de búsqueda directamente para teclear el event
# TODO: cuando hacemos clic en el botón de la cuota para hacer la selección, aparece un modal para colocar el stake, 
# directamente para escribir la cantidad a apostar. comprobar si dando enter se hace la apuesta