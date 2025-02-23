from entity.pick.pick import Pick
from entity.user import User

class Bet:

    Pick : Pick
    User : User
    Stake : float

    PlacedOdd : float
    IsUnderMinOdds : bool = False
    PlacingError : bool = False # TODO: tener un BetErrorEnum
    IsPlaced : bool = False
    Result : str

    def __init__(self, pick : Pick, user : User, stake : float):
        self.Pick = pick
        self.User = user
        self.Stake = stake

    def to_dict(self):
        return {
            "Pick":self.Pick,
            "User": self.User.to_dict() if self.User else "",
            "Stake": self.Stake if self.Stake else -1,

            "PlaceOdd": self.PlacedOdd if self.PlacedOdd else -1,
            "IsUnderMinOdds": self.IsUnderMinOdds if self.IsUnderMinOdds else False,
            "PlacingError": self.PlacingError if self.PlacingError else False,
            "IsPlaced": self.IsPlaced if self.IsPlaced else False,
            "Result": self.IsPlaced if self.IsPlaced else ""
        }
