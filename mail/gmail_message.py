
class GmailMessage:

    MessageObj = None

    Subject : str
    From : str
    To : str
    Date : str
    UID : int
    MessageHtml : str

    def __init__(self, message_obj):
        if message_obj is None:
            raise Exception("Cannot create a GmailMessage object from a void Message.") # TODO: mejorar

        self.MessageObj = message_obj
        self.set_message_values()

    def set_message_values(self):
        self.Subject = self.MessageObj["Subject"]
        self.From = self.MessageObj["From"]
        self.To = self.MessageObj["To"]
        self.Date = self.MessageObj["Date"]
        self.UID = self.MessageObj["UID"]
        self.set_message_html()

    def set_message_html(self) -> None:
        self.MessageHtml = str(self.MessageObj.get_payload())
        # self.MessageHtml = str(self.MessageObj.get_payload()[1])  # para mensajes reenviados

    def __str__(self):
        return self.MessageHtml


#"password": "google8ARE#smbot"
