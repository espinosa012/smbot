
class User:
    Url : str
    Username : str
    Password : str
    DefaultStake : float
    IsActive : bool

    def __init__(self, url : str, username : str, password : str, default_stake : float = 0, is_active : bool = True):
        self.Url = url
        self.Username = username
        self.Password = password
        self.DefaultStake = default_stake
        self.IsActive = is_active

    def to_dict(self):
        return {
            "Url": self.Url,
            "Username": self.Username,
            "Password": self.Password,
            "IsActive": self.IsActive
        }