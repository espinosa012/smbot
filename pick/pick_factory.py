from bs4 import BeautifulSoup

from entity.pick.pick import Pick
from mail.gmail_message import GmailMessage


# BETAMINIC
def get_betaminic_picks_from_message(message: GmailMessage) -> list:
    message_picks: list = []
    soup = BeautifulSoup(message.MessageHtml, 'html.parser')
    for ul in soup.find_all("ul"):
        pick: Pick = Pick()
        values = [t.strip() for t in ul.text.strip().split("=09")]
        pick.Date = f"{values[0].split(":")[1].strip()}"
        pick.Time = f"{values[1].split("):")[1].strip()}"
        pick.Event = values[4].split(":")[1].strip()
        pick.ParticipantNames = get_betaminic_pick_participants(pick.Event)
        set_betaminic_pick_market_and_selection(pick, pick.ParticipantNames, values[5].strip().split(":")[1].strip())
        pick.MinOdds = float(values[6].split(":")[1].strip())
        pick.UID = message.UID
        pick.BetaminicStrategy = get_betaminic_strategy(message.Subject)
        message_picks.append(pick)

    return message_picks

def get_betaminic_pick_participants(event_string : str) -> list:
    special_cases_translation : dict = {"QPR":"Queens Park Rangers"}    # ir agregando. Din. = Dinamo ... podríamos tener esto en db o config
    participants : list = [p.strip() for p in event_string.split(" - ")]
    for p in participants:
        for sct in special_cases_translation.keys():
            if p == sct:
                participants[participants.index(p)] = special_cases_translation[sct]
    return participants

def set_betaminic_pick_market_and_selection(pick: Pick, participants: list, message_bet_string: str):
    # TODO: mover de aquí los flags
    if message_bet_string in participants or ("empate" in message_bet_string.lower() and "(empate apuesta no " not in message_bet_string.lower()):
        pick.Bet["Market"] = "1X2"
        if "empate" in message_bet_string.lower():
            pick.Bet["Selection"] = "D"
        elif participants.index(message_bet_string) == 0:
            pick.Bet["Selection"] = "H"
        else:
            pick.Bet["Selection"] = "A"
    elif "+" in message_bet_string.lower() or "-" in message_bet_string.lower() or "(empate apuesta no " in message_bet_string.lower():
        pick.Bet["Market"] = "AH"
        if "(empate apuesta no " in message_bet_string.lower():
            if " local " in message_bet_string.lower():
                pick.Bet["Selection"] = "H +0"  # TODO: probar
            if " visitante " in message_bet_string.lower():
                pick.Bet["Selection"] = "A +0"

    elif ("m=e1s " in message_bet_string.lower() or "menos " in message_bet_string.lower()) and " goles" in message_bet_string.lower():
        pick.Bet["Market"] = "TG"
        if "m=e1s " in message_bet_string.lower():
            pick.Bet["Selection"] = f"OVER {message_bet_string.lower().replace("m=e1s ", "")
            .replace(" goles", "").strip()}"
        elif "menos " in message_bet_string.lower():
            pick.Bet["Selection"] = f"UNDER {message_bet_string.lower().replace("menos ", "")
            .replace(" goles", "").strip()}"

# TODO
def is_betaminic_1x2_pick(message_bet_string: str, participants: list):
    return message_bet_string in participants or ("empate" in message_bet_string.lower())

def get_betaminic_strategy(message_subject: str):
    return message_subject.split(" Estrategia ")[1].replace('"', "").replace("\r\n", "").strip()
