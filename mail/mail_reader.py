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
    SleepTime : str

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

    def get_current_message_ids(self) -> list:
        return self.Connection.search(None, self.Filter)[1][0].split()
    
    def get_message_by_id(self, id : int):
        _type, data = self.Connection.fetch(id, "(RFC822)")
        return email.message_from_bytes(data[0][1])

    def watch_inbox(self):
        self.Connection.select(self.MailBox)
        print("Listening inbox...")
    
        last_id = self.get_most_recent_message_id()
        
        while True:
            self.Connection.select(self.MailBox)
            if last_id != self.get_most_recent_message_id():
                last_id = self.get_most_recent_message_id()
                msg_obj = self.get_message_by_id(last_id)
                print("new message")
                msg = GmailMessage(msg_obj)
                print(msg)




                # print(msg.Body)
                # TODO: emitir mensaje con redis para que se reciba en el proceso del bot de selenium
    
            time.sleep(self.SleepTime)            

        # aquí, podríamos hacer un return del GmailMessage en el momento en que llegue uno nuevo            

            

    # TODO: crear un método que se ponga a escuchar y devuelva el objeto GmailMessage correspondiente cuando llegue 
    # un nuevo mensaje de pick. ahi se para la escucha, y hay que volverlo a poner a escuchar


