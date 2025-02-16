import email
import imaplib
import json
import time
import requests

from pick import pick_factory
from entity.pick import Pick
from mail.gmail_message import GmailMessage


class MailReader:
    Email: str
    Password: str
    Connection: imaplib.IMAP4_SSL
    Filter: str  # "ALL", "UNSEEN", ...
    MailBox: str  # "INBOX", ...
    CredentialsFilePath: str
    SleepTime: int
    IsWatching: bool

    def __init__(self, _filter: str = "ALL", mail_box: str = "INBOX", sleep_time: int = 5):
        self.Email, self.Password = self.get_credentials()
        self.Filter = _filter
        self.MailBox = mail_box
        self.SleepTime = sleep_time

    @staticmethod
    def get_server_address() -> str:
        with open("config/config.json", "r") as creds_file:
            return json.load(creds_file)["server"]["address"]

    @staticmethod
    def get_credentials():
        with open("config/config.json", "r") as creds_file:
            creds = json.load(creds_file)["email_credentials"]
        return creds["email"], creds["app_password"]

    def connect(self):
        self.Connection = imaplib.IMAP4_SSL("imap.gmail.com")
        self.Connection.login(self.Email, self.Password)

    # Reading messages
    def get_most_recent_message_id(self):
        ids = self.get_current_message_ids()
        if ids:
            return ids[-1]
        return None

    def get_current_message_ids(self) -> list:
        return self.Connection.uid("search", None, self.Filter)[1][0].split()

    def get_message_by_id(self, uid: int):
        try:
            # _type, data = self.Connection.fetch(_id, "(RFC822)")
            _type, data = self.Connection.uid("fetch", uid, "(RFC822)")
            msg_obj = email.message_from_bytes(data[0][1])
            msg_obj["UID"] = int(uid)
            return msg_obj
        except Exception as e:
            print(e)  # TODO: al logger
        return None

    def watch(self):
        self.IsWatching = True
        while self.IsWatching:
            self.Connection.select(self.MailBox)
            # actualizamos la lista de ids, si hay alguna nueva, las vamos procesando
            processed_ids: list = []  # TODO: quizás podríamos obtener las ids procesadas al arrancar consultando en db
            # obtenemos la lista de ids a procesar, que serán las que estén en la bandeja de entrada y no en processed_ids
            new_messages_ids: list = self.get_new_messages_ids(processed_ids)
            # procesamos las ids no procesadas y lanzamos los picks, con redis o lo que sea.
            self.process_messages(new_messages_ids, processed_ids)
            time.sleep(self.SleepTime)

    def get_new_messages_ids(self, already_processed_ids: list):
        new_messages_ids: list = list(set(self.get_current_message_ids()) - set(already_processed_ids))
        if new_messages_ids:
            pass  # TODO: indicar en logger la llegada de nuevos mensajes
        return new_messages_ids

    def process_messages(self, message_ids: list, already_processed_ids: list):
        for _id in message_ids:
            already_processed_ids.append(_id)
            msg_obj = self.get_message_by_id(_id)
            if msg_obj and self.is_pick_message(msg_obj):
                # si es un mensaje de pick, formamos la lista de objetos picks
                for mp in pick_factory.get_betaminic_picks_from_message(GmailMessage(msg_obj)):
                    # TODO: lo guardamos en la base de datos y emitimos con redis un mensaje con la id que tiene en db
                    # TODO: hay que paralelizar esto
                    self.emit_pick(mp)

    def emit_pick(self, pick: Pick):
        try:
            response = requests.post(f"{self.get_server_address()}/place-pick", data=json.dumps(pick.to_dict()),
                          headers={'Content-Type': 'application/json'})
            print(response)
        except requests.exceptions.ConnectionError as conn_err:
            print(conn_err) # TODO: al logger y gestionar bien

    @staticmethod
    def is_pick_message(msg: email.message.Message):
        return "Picks" in msg["Subject"].strip()
