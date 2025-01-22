import time
import random
import undetected_chromedriver as uc    # TODO: mirar v2 https://pypi.org/project/undetected-chromedriver/2.1.1/
from selenium.webdriver import ChromeOptions
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

    

# TODO: necesito comprobar el user agent de undetected, con wireshark o lo que sea

def get_driver() -> uc.Chrome:
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--incognito")
    return uc.Chrome(chrome_options )


def wait_element_clickable(driver : Chrome, xpath : str, timeout : int = 10) -> None:
    try:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    except:
        pass # TODO: indicar en logger que el elemento no es clickable tras espera

def wait_element_visible(driver : Chrome, xpath : str, timeout : int = 10, retry : bool = False) -> None:
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(By.XPATH, xpath))
    except:
        pass # TODO: indicar en logger que no ha aparecido en el tiempo indicado, quizás contemplar la opción de reintentar
        
def wait_element_invisible(driver : Chrome, xpath : str, timeout : int = 10) -> None:
    try:
        WebDriverWait(driver, timeout).until(EC.invisibility_of_element_located(By.XPATH, xpath))
    except:
        pass # TODO: indicar en logger que el elemento no ha desaparecido

def is_element_present(driver : Chrome, xpath : str, timeout : int = 10) -> bool:
    try:
        WebDriverWait(driver, timeout).until(EC.presence_of_element_located(By.XPATH, xpath))
        return True
    except:
        return False

def find_element_by_xpath(driver : Chrome, xpath : str, timeout : int = 10) -> None:
    if is_element_present(driver, xpath, timeout):
        return driver.find_element(By.XPATH, xpath)
    else:
        return None

def click(driver, xpath : str, timeout=10) -> Chrome:
    wait_element_clickable(driver, xpath, timeout)
    find_element_by_xpath(driver, xpath).click()

def clear(driver, xpath : str, timeout=10) -> None:
    find_element_by_xpath(driver, xpath, timeout).clear()

def send_keys(driver, xpath : str, value : str, timeout=10) -> None:
    for char in value:
        find_element_by_xpath(driver, xpath, timeout).send_keys(char)
        time.sleep(random.uniform(0.02, 0.43))

# TODO: necesitamos funciones para buscar por texto y otro para devolver la posición de un web element