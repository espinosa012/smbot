import json
import imaplib
import email
from email.header import decode_header

class MailReader:

    Email : str
    Password : str
    Connection : imaplib.IMAP4_SSL

    def __init__(self):
        self.Email, self.Password = self.get_credentials()

    def get_credentials(self, filename = "mail/credentials.json"):
        creds = None
        with open(filename, "r") as creds_file:
            creds = json.load(creds_file)
        return creds["email"], creds["app_password"]

    def connect(self):
        self.Connection = imaplib.IMAP4_SSL("imap.gmail.com")
        self.Connection.login(self.Email, self.Password)

    def get_most_recent_message_id(self):
        return self.get_current_message_ids()[-1]

    def get_current_message_ids(self, filter : str = "UNSEEN") -> list:
        return self.Connection.search(None, filter)[1][0].split()
    
    def get_message_by_id(self, id, format : str = "(RFC822)"):
        msg_data = mail.fetch(id, format)[1]

    def watch_inbox(self, mailbox_name : str = "inbox"):
        self.Connection.select(mailbox_name)
        messages = self.get_current_message_ids()
        last_message_id = self.get_most_recent_message_id()



        print(last_message_id)
        print(messages)





    


