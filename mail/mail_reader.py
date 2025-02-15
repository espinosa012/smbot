import time
import json
import imaplib
import email

from data.redis_handler import RedisHandler
from mail.gmail_message import GmailMessage

class MailReader:
    Email: str
    Password: str
    Connection: imaplib.IMAP4_SSL
    Filter: str  # "ALL", "UNSEEN", ...
    MailBox: str  # "INBOX", ...
    CredentialsFilePath: str
    SleepTime: int
    RedisConn: RedisHandler

    def __init__(self, _filter: str = "ALL", mail_box: str = "INBOX",
                 sleep_time: int = 5):
        self.Email, self.Password = self.get_credentials()
        self.Filter = _filter
        self.MailBox = mail_box
        self.SleepTime = sleep_time
        self.redis_setup()

    def redis_setup(self):
        with open("config/config.json", "r") as creds_file:
            redis_config = json.load(creds_file)["redis"]
        self.RedisConn = RedisHandler(str(redis_config["host"]), int(redis_config["port"]), int(redis_config["db"]))

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
            print(e)    # TODO: al logger
        return None

    def watch(self):
        while True:
            self.Connection.select(self.MailBox)
            # actualizamos la lista de ids, si hay alguna nueva, las vamos procesando
            processed_ids: list = []    # TODO: quizás podríamos obtener las ids procesadas al arrancar consultando en db
            new_ids: list = self.get_current_message_ids()
            # obtenemos la lista de ids a procesar, que serán las que estén en la bandeja de entrada y no en processed_ids
            ids_to_process: list = list(set(new_ids) - set(processed_ids))
            # procesamos las ids no procesadas y lanzamos los picks, con redis o lo que sea.
            self.process_ids(ids_to_process)
            time.sleep(self.SleepTime)

    def process_ids(self, ids_to_process : list):
        for _id in ids_to_process:
            msg_obj = self.get_message_by_id(_id)
            if msg_obj and self.is_pick_message(msg_obj):
                # si es un mensaje de pick, formamos la lista de objetos picks
                for mp in GmailMessage(msg_obj).get_picks_from_message():
                    # TODO: lo guardamos en la base de datos y emitimos con redis un mensaje con la id que tiene en db
                    self.RedisConn.emit_pick_message(mp)
                    pass

    @staticmethod
    def is_pick_message(msg : email.message.Message):
        return "Picks" in msg["Subject"].strip()