
class User:
    Url : str
    Username : str
    Password : str

    def __init__(self, url : str, username : str, password : str):
        self.Url = url
        self.Username = username
        self.Password = password