from bs4 import BeautifulSoup

from entity.pick import Pick
from mail.gmail_message import GmailMessage


# BETAMINIC
def get_betaminic_picks_from_message(message : GmailMessage) -> list:
    message_picks: list = []
    soup = BeautifulSoup(message.MessageHtml, 'html.parser')
    for ul in soup.find_all("ul"):
        pick: Pick = Pick()
        values = [t.strip() for t in ul.text.strip().split("=09")]
        pick.Date = f"{values[0].split(":")[1].strip()} {values[1].split("):")[1].strip()}"
        pick.Event = values[4].split(":")[1].strip()
        pick.Participants = [p.strip() for p in pick.Event.split(" - ")]
        set_betaminic_pick_market(pick, pick.Participants, values[5].strip().split(":")[1].strip())
        pick.MinOdds = float(values[6].split(":")[1].strip())
        pick.MessageId = message.UID
        pick.BetaminicStrategy = get_betaminic_strategy(message.Subject)
        message_picks.append(pick)

    return message_picks

def set_betaminic_pick_market(pick: Pick, participants: list, message_bet_string: str):
    if message_bet_string in participants or "empate" in message_bet_string.lower():
        pick.Bet["market"] = "1X2"
        if "empate" in message_bet_string.lower():
            pick.Bet["selection"] = "D"
        elif participants.index(message_bet_string) == 0:
            pick.Bet["selection"] = "H"
        else:
            pick.Bet["selection"] = "A"
    elif "+" in message_bet_string.lower() or "-" in message_bet_string.lower():
        pick.Bet["market"] = "AH"
    elif (
            "m=e1s " in message_bet_string.lower() or "menos " in message_bet_string.lower()) and " goles" in message_bet_string.lower():
        pick.Bet["market"] = "TG"
        if "m=e1s " in message_bet_string.lower():
            pick.Bet["selection"] = f"OVER {message_bet_string.lower().replace("m=e1s ", "")
            .replace(" goles", "").strip()}"
        elif "menos " in message_bet_string.lower():
            pick.Bet["selection"] = f"UNDER {message_bet_string.lower().replace("menos ", "")
            .replace(" goles", "").strip()}"

def get_betaminic_strategy(message_subject : str):
    return message_subject.split(" Estrategia ")[1].replace('"', "").strip()

