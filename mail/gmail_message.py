from bs4 import BeautifulSoup

from pick.pick import Pick


class GmailMessage:

    MessageObj = None

    Subject : str
    From : str 
    To : str 
    Date : str 
    UID : int
    MessageHtml : str

    def __init__(self, message_obj):
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
        self.MessageHtml = str(self.MessageObj.get_payload()[1])

    # TODO: llevar fuera de aquí
    def get_picks_from_message(self) -> list:
        message_picks : list = []
        # llevar a pick
        soup = BeautifulSoup(self.MessageHtml, 'html.parser')
        for ul in soup.find_all("ul"):
            pick: Pick = Pick()
            values = [t.strip() for t in ul.text.strip().split("=09")]
            pick.Event = values[4].split(":")[1].strip()
            pick.Participants = [p.strip() for p in pick.Event.split(" - ")]
            self.set_pick_market(pick, pick.Participants, values[5].strip().split(":")[1].strip())
            pick.MinOdds = float(values[6].split(":")[1].strip())
            pick.MessageId = self.UID
            message_picks.append(pick)

        return message_picks

    @staticmethod
    def set_pick_market(pick : Pick, participants : list, message_bet_string : str):
        if message_bet_string in participants or " draw" in message_bet_string.lower() or " empate" in message_bet_string.lower():
            pick.Bet["market"] = "1X2"
            if " draw" in message_bet_string.lower():
                pick.Bet["selection"] = "D"
            elif participants.index(message_bet_string) == 0:
                pick.Bet["selection"] = "H"
            else:
                pick.Bet["selection"] = "A"
        elif "over " in message_bet_string.lower() or "under " in message_bet_string.lower():
            pick.Bet["market"] = "TG"
        elif "+" in message_bet_string.lower() or "-" in message_bet_string.lower():
            pick.Bet["market"] = "AH"

    def __str__(self):
        return self.MessageHtml
    

#"password": "google8ARE#smbot"
