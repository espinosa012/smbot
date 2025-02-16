from entity.user import User

class Bet:
    PickList : list
    User : User
    Stake : float

    def __init__(self, picks : list, user : User, stake : float):
        self.PickList = picks
        self.User = user
        self.Stake = stake