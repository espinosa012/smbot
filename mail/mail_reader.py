import email
import imaplib
import json
import time
from mailbox import Message

import requests

from pick import pick_factory
from entity.pick.pick import Pick
from mail.gmail_message import GmailMessage

class MailReader:
    Email: str
    Password: str
    Connection: imaplib.IMAP4_SSL
    Filter: str  # "ALL", "UNSEEN", ...
    MailBox: str  # "INBOX", ...
    CredentialsFilePath: str
    SleepTime: int
    IsWatching: bool = False

    def __init__(self, _filter: str = "ALL", mail_box: str = "INBOX", sleep_time: int = 5):
        self.Email, self.Password = self.get_credentials()
        self.Filter = _filter
        self.MailBox = mail_box
        self.SleepTime = sleep_time

    @staticmethod
    def get_server_address() -> str:
        # TODO: tomar ruta absoluta respecto del fichero
        with open("config/config.json", "r") as creds_file:
            return json.load(creds_file)["server"]["address"]

    @staticmethod
    def get_credentials():
        # TODO: tomar ruta absoluta respecto del fichero
        with open("config/config.json", "r") as creds_file:
            creds = json.load(creds_file)["email_credentials"]
        return creds["email"], creds["app_password"]

    def connect(self):
        self.Connection = imaplib.IMAP4_SSL("imap.gmail.com")
        self.Connection.login(self.Email, self.Password)

    # Reading messages
    def retrieve_inbox_messages(self) -> list:
        # TODO: UNTESTED. la idea es usarlo para tomar los mensajes sin necesidad de ponerlo a escuchar, hacerlo una única vez
        # No previous connection required
        self.connect()
        current_gmail_messages : list = []
        for _id in self.get_current_message_ids():
            msg_obj : Message = self.get_message_by_id(_id)
            if bool(msg_obj): current_gmail_messages.append(GmailMessage(msg_obj))
        return current_gmail_messages


    def get_current_message_ids(self) -> list:
        """ Devuelve las ids de los mensajes del filtro 'Filter', por defecto ALL"""
        # noinspection PyTypeChecker
        return self.Connection.uid("search", None, self.Filter)[1][0].split()

    def get_message_by_id(self, uid: int) -> Message:
        """ Devuelve el mensaje (mailbox.Message) con id única igual a uid """
        try:
            # noinspection PyTypeChecker
            _type, data = self.Connection.uid("fetch", uid, "(RFC822)")
            msg_obj : Message = email.message_from_bytes(data[0][1])
            msg_obj["UID"] = int(uid)
            return msg_obj
        except Exception as e:
            print(e)  # TODO: al logger
        return None

    def get_new_messages_ids(self, already_processed_ids: list = None):
        """ Devuelve la lista de ids únicas correspondientes a los mensajes del MailBox que aún no hayan sido procesados."""
        new_messages_ids: list = []
        # if bool(already_processed_ids): new_messages_ids = list(set(self.get_current_message_ids()) - set(already_processed_ids))
        new_messages_ids = list(set(self.get_current_message_ids()) - set(already_processed_ids))
        if len(new_messages_ids) != 0:
            new_messages_ids.sort()
            pass  # TODO: indicar en logger la llegada de nuevos mensajes
        return new_messages_ids

    def stop_watching(self):
        self.IsWatching = False

    def watch(self, process_previous_messages : bool = False):
        # TODO: gestionar los errores por pérdida de conexión. Reintentar cada x tiempo mientras IsWatching
        """ Se mantiene monitorizando el buzón 'MailBox' (por defecto INBOX) mientras IsWatching es True. Para cada
            conjunto de mensajes recibidos durante el tiempo de pausa, llama al mét odo process_messages"""
        self.IsWatching = True
        self.Connection.select(self.MailBox)
        processed_ids: list = []
        # if not process_previous_messages: processed_ids = self.get_current_message_ids()
        print(list(set(self.get_current_message_ids()) - set(processed_ids)))
        while self.IsWatching:
            self.Connection.select(self.MailBox)
            # actualizamos la lista de ids, si hay alguna nueva, las vamos procesando
            # obtenemos la lista de ids a procesar, que serán las que estén en la bandeja de entrada y no en processed_ids
            new_messages_ids: list = self.get_new_messages_ids(processed_ids)
            # procesamos las ids no procesadas y lanzamos los picks, con redis o lo que sea.
            self.process_messages(new_messages_ids, processed_ids)
            time.sleep(self.SleepTime)

    def process_messages(self, message_ids: list, already_processed_ids: list):
        """ Procesa un conjunto de mensajes. En cada mensaje puede venir más de un pick"""
        for _id in message_ids:
            already_processed_ids.append(_id)   # TODO: a lo mejor es mejor que la lista de ids procesadas se defina en el servidor
            self.process_message(self.get_message_by_id(_id))

    def process_message(self, msg_obj : Message):
        """ Procesa un mensaje individual """
        if msg_obj and self.is_pick_message(msg_obj):
            # si es un mensaje de pick, formamos la lista de objetos picks
            message_picks: list = pick_factory.get_betaminic_picks_from_message(GmailMessage(msg_obj))
            for mp in message_picks:
                self.process_pick(mp)

    def process_pick(self, pick: Pick):
        """ Procesa un pick individual (almacenamiento, notificación, emisión...) """
        print(f"Incoming pick: {pick.Event}, {pick.Bet["Market"]}-{pick.Bet["Selection"]}")  # TODO: al logger
        try:
            requests.post(f"{self.get_server_address()}/process-pick", data=json.dumps(pick.to_dict()),
                          headers={'Content-Type': 'application/json'})
        except requests.exceptions.ConnectionError as conn_err:
            print(conn_err)  # TODO: error al logger y gestionar bien

    def emit_pick(self, pick: Pick):
        """ Para enviar un pick al endpoint de colocación. """
        try:
            # TODO: parametrizar el endpoint, tomar de configuración o lo que sea.
            response = requests.post(f"{self.get_server_address()}/place-pick", data=json.dumps(pick.to_dict()),
                          headers={'Content-Type': 'application/json'})
        except requests.exceptions.ConnectionError as conn_err:
            print(conn_err) # TODO: error al logger y gestionar bien

    @staticmethod
    def is_pick_message(msg: email.message.Message):
        """ Determinar si un mensaje se corresponde con un mensaje de pick o no. """
        # TODO: usar from, añadir lista de destinatarios (To) posibles para mensajes de pick
        return msg["To"].strip() == "juamvu@gmail.com"
