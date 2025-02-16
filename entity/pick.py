

class Pick:
    
    Date : str
    Event : str
    Participants : list = []
    Bet : dict = {} # {market, selection}
    MinOdds : float
    Stake : float   # cantidad a apostar en términos absolutos ??
    BetaminicStrategy : str
    MessageId : int

    def __init__(self, json_pick : dict = None):
        self.Date = json_pick["Date"] if json_pick else ""
        self.Event = json_pick["Event"] if json_pick else ""
        self.Participants = json_pick["Participants"] if json_pick else []
        self.Bet = json_pick["Bet"] if json_pick else {"market":"", "selection":""}
        self.MinOdds = json_pick["MinOdds"] if json_pick else 0
        self.Stake = json_pick["Stake"] if json_pick else 0
        self.BetaminicStrategy = json_pick["BetaminicStrategy"] if json_pick else ""
        self.MessageId = json_pick["MessageId"] if json_pick else -1

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