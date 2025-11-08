from db import db

class LoginManager():
    def __init__(self):
        self.my_db = db.db()
        self.df = self.my_db.query("SELECT user_name, user_password FROM `Users`")

    def auth(self, username: str, password:str) -> bool:
        '''Trả về true nếu username và password ở trong db và ngược lại'''
        if self.df is None or self.df.empty:
            return False

        matching_user = self.df[
            (self.df["user_name"] == username) & 
            (self.df["user_password"] == password)
        ]

        return not matching_user.empty

class SigninManager():
    def __init__(self):
        my_db = db.db()
        self.df = my_db.query("SELECT user_email, user_name, user_password  FROM `Users`")
    
    def check_if_exists(self, email: str, user_name: str, pwd: str) -> int:
        '''Trả về 0 nếu oke, trả về 1 nếu email đã tồn tại, trả về 2 nếu username đã tồn tại'''
        if email in self.df["user_email"]:
            return 1
        elif user_name in self.df["user_name"]:
            return 2
        return 0
    
    def update_db(self):
        pass
