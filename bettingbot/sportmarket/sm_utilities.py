
import bettingbot.selenium_utilities as selenium_utilities
import bettingbot.sportmarket.pageobject as sm_pageobject 


def login(driver, username : str, password : str):
    # wait_element_clickable(driver, LOGIN_BUTTON)
    # send_keys(driver, LOGIN_USERNAME, username)
    # send_keys(driver, LOGIN_PASSWORD, password)
    # click(driver, LOGIN_BUTTON)

    # hacer clic, con nuestro método para mover el ratón hasta la posición,  en un lugar aleatorio del cuadro de texto de usuario (offset aleatorio del centro o la posición que devuelva selenium)
    # usando nuestra manera con paradas aleatorias, introducir nombre de usuario
    # espera aleatoria de entorno a 0.7s antes de hacer clic en el ionput de la contraseña, con el método para mover el ratón
    # repetir los pasos anteriores para la controseña
    # otra espeara aleatoria similar y clic en el botón de login (podríamos meter la espera en el propio método de click)
    # esperar con selenium a que se muestre el home
    pass

def search_event(driver, event : str) -> None:
    # ctrl + f para mostrar el modal
    # esperamos un pequeño tiempo aleatorio
    # introducimos la cadena del evento
    pass

def check_odds(driver, min_odds : float) -> bool:
    return get_odds() >= min_odds

def get_odds(driver) -> float: 
    return 0



# TODO: con ctrl+f aparece el cuadro de búsqueda directamente para teclear el event
# TODO: cuando hacemos clic en el botón de la cuota para hacer la selección, aparece un modal para colocar el stake, 
# directamente para escribir la cantidad a apostar. comprobar si dando enter se hace la apuesta