import time
import random
import undetected_chromedriver as uc    # TODO: mirar v2 https://pypi.org/project/undetected-chromedriver/2.1.1/
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException


# TODO: necesito comprobar el user agent de undetected, con wireshark o lo que sea
# TODO: meter logger

def get_driver() -> uc.Chrome:
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver : uc.Chrome = uc.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.implicitly_wait(10)
    return driver

def close_driver(driver : uc.Chrome) -> None:
    driver.close()

def wait_element_clickable(driver : uc.Chrome, xpath : str, timeout : int = 10) -> None:
    try:
        WebDriverWait(driver, timeout).until(ec.element_to_be_clickable((By.XPATH, xpath)))
    except TimeoutException  :
        pass # TODO: indicar en logger que el elemento no es clickable tras espera

def wait_element_visible(driver : uc.Chrome, xpath : str, timeout : int = 10, retry : bool = False) -> None:
    try:
        WebDriverWait(driver, timeout).until(ec.visibility_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        if retry:
            try:
                WebDriverWait(driver, timeout).until(ec.visibility_of_element_located((By.XPATH, xpath)))
            except TimeoutException:
                pass # TODO: indicar en logger que no ha aparecido en el tiempo indicado, quizás contemplar la opción de reintentar
        
def wait_element_invisible(driver : uc.Chrome, xpath : str, timeout : int = 10) -> None:
    if xpath:
        try:
            driver.implicitly_wait(timeout)
            WebDriverWait(driver, timeout).until(ec.invisibility_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            pass # TODO: indicar en logger que el elemento no ha desaparecido

def is_element_present(driver : uc.Chrome, xpath : str) -> bool:
    return bool(driver.find_elements(By.XPATH, xpath))

def find_element_by_xpath(driver : uc.Chrome, xpath : str, retry : bool = False) -> WebElement | None:
    if is_element_present(driver, xpath):
        return driver.find_element(By.XPATH, xpath)
    elif retry:
        return find_element_by_xpath(driver, xpath, False)
        # TODO: indicar en logger que no se ha encontrado el elemento a clickar

def find_elements_by_xpath(driver :uc.Chrome, xpath : str) -> list:
    return driver.find_elements(By.XPATH, xpath)

def find_element_by_partial_text(driver : uc.Chrome, xpath : str, text : str) -> WebElement | None:
    for elem in driver.find_elements(By.XPATH, xpath):
        if text in elem.get_attribute("text"):  
            return elem
    return None # TODO: untested

def selenium_click(driver : uc.Chrome, xpath : str, timeout=10) -> None:
    wait_element_clickable(driver, xpath, timeout)
    time.sleep(random.uniform(0.1, 0.3))
    find_element_by_xpath(driver, xpath).click()

def selenium_clear_input(driver : uc.Chrome, xpath : str) -> None:
    elem : WebElement = find_element_by_xpath(driver, xpath, True)
    if elem:
        time.sleep(0.12)
        elem.clear()

def selenium_send_keys(driver : uc.Chrome, xpath : str, value : str) -> None:
    elem = find_element_by_xpath(driver, xpath, False)
    for char in str(value):
        elem.send_keys(char)
        time.sleep(random.uniform(0.04, 0.23))
    time.sleep(random.uniform(0.4, 0.7))    # TODO: parametrizar la espera
    
def save_screenshot(driver : uc.Chrome):
    #TODO
    pass
