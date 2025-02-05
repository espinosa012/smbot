import time
import random
import undetected_chromedriver as uc    # TODO: mirar v2 https://pypi.org/project/undetected-chromedriver/2.1.1/
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
    

# TODO: necesito comprobar el user agent de undetected, con wireshark o lo que sea
# TODO: meter logger

def get_driver() -> uc.Chrome:
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--incognito")
    return uc.Chrome(options=chrome_options)
    # return uc.Chrome()

def close_driver(driver : uc.Chrome) -> None:
    driver.close()

def wait_element_clickable(driver : uc.Chrome, xpath : str, timeout : int = 10) -> None:
    try:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    except:
        pass # TODO: indicar en logger que el elemento no es clickable tras espera

def wait_element_visible(driver : uc.Chrome, xpath : str, timeout : int = 10, retry : bool = False) -> None:
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(By.XPATH, xpath))
    except:
        pass # TODO: indicar en logger que no ha aparecido en el tiempo indicado, quizás contemplar la opción de reintentar
        
def wait_element_invisible(driver : uc.Chrome, xpath : str, timeout : int = 10) -> None:
    try:
        WebDriverWait(driver, timeout).until(EC.invisibility_of_element_located(By.XPATH, xpath))
    except:
        pass # TODO: indicar en logger que el elemento no ha desaparecido

def is_element_present(driver : uc.Chrome, xpath : str, timeout : int = 10) -> bool:
    return bool(driver.find_elements(By.XPATH, xpath))

def find_element_by_xpath(driver : uc.Chrome, xpath : str, timeout : int = 10) -> None:
    if is_element_present(driver, xpath, timeout):
        return driver.find_element(By.XPATH, xpath)
    else:
        return None # TODO: indicar en logger que no se ha encontrado el elemento a clickar

def find_element_by_partial_text(driver : uc.Chrome, xpath : str, text : str):
    for elem in driver.find_elements(By.XPATH, xpath):
        if text in elem.get_attribute("text"):  
            return elem
    return None # TODO: untested

def selenium_click(driver : uc.Chrome, xpath : str, timeout=10):
    wait_element_clickable(driver, xpath, timeout)
    time.sleep(random.uniform(0.1, 0.3))
    find_element_by_xpath(driver, xpath).click()

def selenium_clear_input(driver : uc.Chrome, xpath : str, timeout=10) -> None:
    find_element_by_xpath(driver, xpath, timeout).clear()

def selenium_send_keys(driver : uc.Chrome, xpath : str, value : str, timeout=10) -> None:
    elem = find_element_by_xpath(driver, xpath, timeout)
    for char in value:
        elem.send_keys(char)
        time.sleep(random.uniform(0.09, 0.43))
    time.sleep(random.uniform(0.5, 1.2))
    
def save_screenshot(driver : uc.Chrome):
    pass


# TODO: usar implicit_wait a nivel  gloabl y quitar los timeout, no parece funcionar bien
# TODO: tomar capturas de pantalla o de webelements concretos 
# TODO: necesitamos funciones para buscar por texto y otro para devolver la posición de un web element