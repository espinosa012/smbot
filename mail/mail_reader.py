import time
import json
import imaplib
import email
from mail.gmail_message import GmailMessage


class MailReader:
    Email: str
    Password: str
    Connection: imaplib.IMAP4_SSL
    Filter: str  # "ALL", "UNSEEN", ...
    MailBox: str  # "INBOX", ...
    CredentialsFilePath: str
    SleepTime: int

    def __init__(self, creds_file_path: str = "config/config.json", _filter: str = "ALL", mail_box: str = "INBOX",
                 sleep_time: int = 5):
        self.Email, self.Password = self.get_credentials()
        self.Filter = _filter
        self.MailBox = mail_box
        self.CredentialsFilePath = creds_file_path
        self.SleepTime = sleep_time

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
        #     TODO cambiar para que coja la id única del mensaje y poder guardar las ids procesadas

    def get_current_message_ids(self) -> list:
        return self.Connection.search(None, self.Filter)[1][0].split()

    # noinspection PyUnresolvedReferences,PyTypeChecker
    def get_message_by_id(self, _id: int):
        # TODO: gestionar la excepción aquí, y no en la llamada
        try:
            _type, data = self.Connection.fetch(_id, "(RFC822)")
            return email.message_from_bytes(data[0][1])
        except Exception as e:
            print(e)    # TODO: al logger
        return None

    def watch(self):
        self.Connection.select(self.MailBox)

        # actualizamos la lista de ids, si hay alguna nueva, las vamos procesando
        processed_ids: list = []    # TODO: quizás podríamos obtener las ids procesadas al arrancar consultando en db
        new_ids: list = self.get_current_message_ids()
        # obtenemos la lista de ids a procesar, que serán las que estén en la bandeja de entrada y no en processed_ids
        ids_to_process: list = list(set(new_ids) - set(
            processed_ids))  # TODO: ordenar antes los sets para ir colocando en el orden de la bandeja de entrada, o el inverso
        # procesamos las ids no procesadas y lanzamos los picks, con redis o lo que sea.
        for _id in ids_to_process:
            # TODO: obtener aqui el msgobj y pasarselo a get_message_picks por eficiencia. puede ser nulo
            if self.is_pick_message(_id):
                # si es un mensaje de pick, formamos la lista de objetos picks
                message_picks: list = self.get_message_picks(_id)
                for mp in message_picks:
                    # TODO: lo guardamos en la base de datos y emitimos con redis un mensaje con la id que tiene en db
                    pass
            # las ids que se van procesando se meten en la lista processed_ids
            processed_ids.append(_id)
        time.sleep(self.SleepTime)

    def get_message_picks(self, _id : int) -> list:
        msg_obj = self.get_message_by_id(_id)
        if msg_obj:
            return GmailMessage(msg_obj).get_picks_from_message()
        return []

    def is_pick_message(self, _id: int):
        # TODO: necesitamos una manera de determinar si es un mensaje de pick; el asunto, algún flag, etc
        return True

