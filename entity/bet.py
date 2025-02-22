from entity.pick.pick import Pick
from entity.user import User

class Bet:

    Pick : Pick
    User : User
    Stake : float

    def __init__(self, picks : Pick, user : User, stake : float):
        self.Pick = picks
        self.User = user
        self.Stake = stake

    def to_dict(self):
        return {
            "Pick":self.Pick,
            "User": self.User.to_dict() if self.User else "",
            "Stake": self.Stake if self.Stake else -1
        }
