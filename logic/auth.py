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
        self.my_db = db.db()
        self.df = self.my_db.query("SELECT user_email, user_name, user_password  FROM `Users`")
    
    def check_if_exists(self, email: str, username: str, pwd: str) -> int:
        '''Trả về 0 nếu oke, trả về 1 nếu email đã tồn tại, trả về 2 nếu username đã tồn tại'''
        if email in self.df["user_email"].values:
            return 1
        elif username in self.df["user_name"].values:
            return 2
        return 0
    
    def add_user(self, username: str, pwd: str, email: str, role = 2) -> bool:
        '''Add user vào db, role 1 là admin, role 2 là user'''
        query = \
                '''INSERT INTO users(user_name, user_password, user_email, user_role_id, user_rank, user_level, user_status) 
                VALUES (%s, %s, %s, %s, 0, 0 , 1)'''
        params = (username, pwd, email, role)
        is_success = self.my_db.dml_ddl_operator(query, params)
        if is_success:
            print("Thêm dữ liệu thành công")
            self.df = self.my_db.query("SELECT user_email, user_name, user_password FROM `users`") # Update
            return True
        return False