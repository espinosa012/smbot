

class Pick:
    
    Date : str
    Event : str
    Participants : list = []
    Bet : dict = {} # {market, selection}
    MinOdds : float
    Stake : float   # cantidad a apostar en términos absolutos ??
    BetaminicStrategy : str
    MessageId : int

    def __init__(self, pick_dict : dict = None):
        self.Date = pick_dict["Date"] if pick_dict else ""
        self.Event = pick_dict["Event"] if pick_dict else ""
        self.Participants = pick_dict["Participants"] if pick_dict else []
        self.Bet = pick_dict["Bet"] if pick_dict else {"market": "", "selection": ""}
        self.MinOdds = pick_dict["MinOdds"] if pick_dict else 0
        self.Stake = pick_dict["Stake"] if pick_dict else 0
        self.BetaminicStrategy = pick_dict["BetaminicStrategy"] if pick_dict else ""
        self.MessageId = pick_dict["MessageId"] if pick_dict else -1

    def from_betaminic(message_body : str):
        # TODO
        pass

    def is_valid_pick(self) -> bool:
        return True

    def to_dict(self):
        return {
            "Date":self.Date,
            "Event":self.Event,
            "Participants":self.Participants,
            "Bet":self.Bet,
            "MinOdds":self.MinOdds,
            "Stake":self.Stake,
            "BetaminicStrategy":self.BetaminicStrategy,
            "MessageId":self.MessageId,
        }

    def __str__(self):
        return str(self.to_dict())