from bs4 import BeautifulSoup
import email

class GmailMessage():

    MessageObj = None

    Subject : str
    From : str 
    To : str 
    Date : str 
    MessageHtml : str 

    def __init__(self, message_obj):
        self.MessageObj = message_obj
        self.set_message_values()

    def set_message_values(self):
        self.Subject = self.MessageObj["Subject"]
        self.From = self.MessageObj["From"]
        self.To = self.MessageObj["To"]
        self.Date = self.MessageObj["Date"]
        self.set_message_body()

    def set_message_html(self) -> None:
        self.MessageHtml = str(self.MessageObj.get_payload()[1])

        # llevar a pick
        # soup = BeautifulSoup(message_content, 'html.parser')
        # for ul in soup.find_all("ul"):
        #     print(ul.prettify())
    

        

        # if len(self.MessageObj.get_payload()) == 2:
        #     self.Body = self.MessageObj.get_payload()[0]

    def get_html_content(self) -> str:
        return ""

    def __str__(self):
        return self.Body
    



    # Scrapping picks