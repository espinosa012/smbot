class Pick:
    # Formato Pick de Betaminic
    Date : str
    Event : str
    Participants : list = []    # TODO: podría llamarse ParticipantNames
    Bet : dict = {} # {market, selection}
    WebParticipantNames : list
    MinOdds : float
    BetaminicStrategy : str
    MessageId : int

    def __init__(self, pick_dict : dict = None):
        self.UID = pick_dict["UID"] if pick_dict else -1
        self.Date = pick_dict["Date"] if pick_dict else ""
        self.Event = pick_dict["Event"] if pick_dict else ""
        self.Participants = pick_dict["Participants"] if pick_dict else []
        self.WebParticipantNames = pick_dict["WebParticipantNames"] if pick_dict else []
        self.Bet = pick_dict["Bet"] if pick_dict else {"Market": "", "Selection": ""}
        self.MinOdds = pick_dict["MinOdds"] if pick_dict else 0
        self.BetaminicStrategy = pick_dict["BetaminicStrategy"] if pick_dict else ""

    # Para enviarlo mediante HTTP
    def to_dict(self):
        return {
            "Date":self.Date,
            "Event":self.Event,
            "Participants":self.Participants,
            "WebParticipantNames":self.WebParticipantNames,
            "Bet":self.Bet,
            "MinOdds":self.MinOdds,
            "BetaminicStrategy":self.BetaminicStrategy,
            "UID": self.UID,
        }

    def __str__(self):
        return str(self.to_dict())