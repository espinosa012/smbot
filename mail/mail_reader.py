import time
import json
import imaplib
import email
from email.header import decode_header
from mail.gmail_message import GmailMessage

class MailReader:

    Email : str
    Password : str
    Connection : imaplib.IMAP4_SSL
    Filter : str    # "ALL", "UNSEEN", ...
    MailBox : str   # "INBOX", ...
    CredentialsFilePath : str # "mail/credentials.json"
    SleepTime : int

    def __init__(self, creds_file_path : str = "mail/credentials.json", filter : str = "ALL", mail_box : str = "INBOX", sleep_time : int = 5):
        self.Email, self.Password = self.get_credentials()
        self.Filter = filter
        self.MailBox = mail_box
        self.CredentialsFilePath = creds_file_path
        self.SleepTime = sleep_time

    def get_credentials(self):
        creds = None
        with open("mail/credentials.json", "r") as creds_file:
            creds = json.load(creds_file)
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
    
    def get_message_by_id(self, id : int):
        _type, data = self.Connection.fetch(id, "(RFC822)")
        return email.message_from_bytes(data[0][1])

    def watch(self):
        self.Connection.select(self.MailBox)
        # actualizamos la lista de ids, si hay alguna nueva, las vamos procesando
        processed_ids : list = []
        new_ids : list = self.get_current_message_ids()
        # obtenemos la lista de ids a procesar, que serán las que estén en la bandeja de entrada y no en processed_ids
        ids_to_process : list = list(set(new_ids) - set(processed_ids))
        # procesamos las ids no procesadas y lanzamos los picks, con redis o lo que sea.
        for _id in ids_to_process:
            if self.is_pick_message(_id):
                # si es un mensaje de pick, formamos la lista de objetos picks
                message_picks : list = []
                try:
                    msg_obj = self.get_message_by_id(_id)   # TODO: puede generar excepción
                    msg = GmailMessage(msg_obj)
                    message_picks = msg.get_picks_from_message()
                    pass
                except Exception as e:
                    print(e)
            # las ids que se van procesando se meten en la lista processed_ids
            processed_ids.append(_id)
        time.sleep(self.SleepTime)

    def is_pick_message(self, _id : int):
        # TODO: necesitamos una manera de determinar si es un mensaje de pick; el asunto, algún flag, etc
        return True

    def watch_inbox(self):
        self.Connection.select(self.MailBox)
        print("Listening inbox...")
    
        last_id = None
        new_last_id = -1
        while True:
            self.Connection.select(self.MailBox)
            if last_id != new_last_id:
                last_id = new_last_id
                try:
                    msg_obj = self.get_message_by_id(last_id)   # TODO: puede generar excepción
                    print("new message")
                except Exception as e:
                    print(e)
                msg = GmailMessage(msg_obj)
                print(msg)
                # print(msg.Body)
                # TODO: emitir mensaje con redis para que se reciba en el proceso del bot de selenium
            time.sleep(self.SleepTime)            
            new_last_id = self.get_most_recent_message_id()

        # aquí, podríamos hacer un return del GmailMessage en el momento en que llegue uno nuevo            

            

    # TODO: crear un método que se ponga a escuchar y devuelva el objeto GmailMessage correspondiente cuando llegue 
    # un nuevo mensaje de pick. ahi se para la escucha, y hay que volverlo a poner a escuchar


