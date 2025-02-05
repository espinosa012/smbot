import random
import pyautogui
import time
from bettingbot.pagui.keys import *
# hacer clic izquierdo
# mover el ratón a una posición siguiendo un patrón humano
# pulsar una única tecla una vez: escape, intro, etc.
# introducir una cadena de texto por teclado con esperas aleatorias entre pulsaciones. introducir errores aleatorios y corregirlos!
# comandos al estilo ctrl+f, ctrl+v, etc
# acciones de más alto nivel, como abrir o cerrar el navegador (aunque probablemente usemos undetected chrome para abrir el navegador), 
#  hacer clic en la barra de búsqueda del navegador, pegar la url del login


# Keys and hotkeys
def ctrlF():
    time.sleep(random.uniform(0.1, 0.4))
    pyautogui.hotkey(CONTROL, 'f')

def escape():
    time.sleep(random.uniform(0.07, 0.12))
    pyautogui.press(ESCAPE)

def type_text(text : str):
    time.sleep(random.uniform(0.07, 0.12))
    pyautogui.typewrite(text)

def random_wait(min : float, max : float):
    random.uniform(min, max)


# TODO: parametrizar las esperas