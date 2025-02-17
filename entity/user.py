
class User:
    Url : str
    Username : str
    Password : str
    IsActive : bool

    def __init__(self, url : str, username : str, password : str, is_active : bool):
        self.Url = url
        self.Username = username
        self.Password = password
        self.IsActive = is_active

    def to_dict(self):
        return {
            "Url": self.Url,
            "Username": self.Username,
            "Password": self.Password,
            "IsActive": self.IsActive
        }