

class Pick:
    
    Date : str
    Event : str
    Participants : list = []
    Bet : dict = {} # {market, selection}
    MinOdds : float
    Stake : float   # cantidad a apostar en términos absolutos ??
    BetaminicStrategy : str

    def __init__(self):
        pass

    def from_betaminic(message_body : str):
        pass

    def is_valid_pick(self) -> bool:
        return False
    

