from entity.user import User

class Bet:
    PickList : list
    User : User
    Stake : float

    def __init__(self, picks : list, user : User, stake : float):
        self.PickList = picks
        self.User = user
        self.Stake = stake

    def to_dict(self):
        pick_list = []
        for p in self.PickList:
            pick_list.append(p.to_dict())
        return {
            "PickList":pick_list,
            "User": self.User.to_dict() if self.User else "",
            "Stake": self.Stake if self.Stake else -1
        }
