from db import db

class LoginManager():
    def __init__(self):
        my_db = db()
        self.df = my_db.query("SELECT username, password FROM `Users`")

    def auth(self, username: str, password:str) -> bool:
        '''Trả về true nếu username và password ở trong db và ngược lại'''
        if self.df is None or self.df.empty:
            return False

        matching_user = self.df[
            (self.df["user_name"] == username) & 
            (self.df["user_password"] == password)
        ]

        return not matching_user.empty

