from db.db import db
from .User import User

class UserManager():
    def __init__(self):
        self. __my_db = db()
        self._df = None
        self.user_list = []
        
        # Lấy thông tin từ db
        self.fetch_db()

    def fetch_db(self):
        '''Lấy thông tin db đưa vào user_list'''
        query = "select * from users"
        try:
            self._df = self.__my_db.query(query=query)
        except Exception as err:
            print(f"Có lỗi xảy ra khi fetch_db trong UserManager. Lỗi {err}")
    
        for i, row in self._df.iterrows():
            user = User(
                user_name= row["user_name"],
                user_password = row["user_password"],
                user_rank = row["user_rank"],
                user_email = row["user_email"],
                user_status = row["user_status"],
                user_role_id = row["user_role_id"],
                user_id = row["user_id"]
            )
            self.user_list.append(user)
    
    def add_user(self, user_name, user_pwd, user_rank, user_email, user_status, user_role_id):
        is_success = user_mgr.add_user(
                    user_name = username, 
                    user_pwd = pwd,
                    user_rank= 0,
                    user_email = email,
                    user_status = 1, 
                    user_role_id= 2
                )

        # Lưu vào db
        query = \
        """insert into users (user_name, user_password, user_rank, user_email, user_status, user_role_id)
            values (%s, %s, %s, %s, %s, %s)"""
        
        params = (user_name, user_pwd, user_rank,user_email, user_status, user_role_id)

        try:
            user_id = self.__my_db.dml_ddl_operator(query, params)

            # Lấy lại user_id của new_user trong db
            new_user = User(
                user_name= user_name,
                user_password= user_pwd,
                user_rank = user_rank,
                user_email = user_email,
                user_status = user_status,
                user_role_id = user_role_id,
                user_id = user_id
            )
            self.user_list.append(new_user)
            return True
        
        except Exception as err:
            print(f"Co loi {err} khi them user {user_name}")
            return False
        

    def find_user_by_id(self, user_id: int):
        '''Tìm thể hiện user dựa theo id, trả về đối tượng nếu có'''
        for user in self.user_list:
            if user_id == user.get_user_id():
                return user
        return None
    
    def auth(self, username: str, password:str):
        '''Trả về user nếu username và password ở trong db và ngược lại'''
        for user in self.user_list:
            if user.get_user_name() == username and user.get_user_password() == password:
                return user
        return False

    def check_email(self, email: str):
        '''Kiểm tra email đã dùng chưa. Trả về True nếu đã được dùng'''
        for user in self.user_list:
            if email == user.get_user_email():
                return True
        return False
    
    def check_user_name(self, user_name: str):
        '''Kiểm tra user_name đã dùng chưa. Trả về True nếu đã được dùng'''
        for user in self.user_list:
            print(user)
            if user.get_user_name() == user_name:
                return True
        return False    
    
    def change_user_status(self, user_id, status):
        '''Thay đổi trạng thái người dùng. Trả về True nếu thay đổi thành công'''
        # Thay đổi trong list
        user = self.find_user_by_id(user_id= user_id)
        if user != None:
            user.set_user_status(status)
        
        # Thay đổi trong db
        query = "update users set user_status = %s where user_id = %s"
        params = (status, user_id)
        try:
            self.__my_db.dml_ddl_operator(query, params)
        except Exception as err:
            print(f"Lỗi khi thay đổi trạng thái người dùng. Lỗi {err}")
            return True
        
if __name__ == "__main__":
    user_mgr = UserManager()
    username = "vy"
    pwd = "vybodoi"
    email = '1@gmail.com'
    status = 1
    role = 2
    # user_mgr.add_user(
    #     user_name= username, 
    #     user_pwd= pwd,
    #     user_email= email,
    #     user_status= status,
    #     user_role_id= role,
    #     user_rank= 0
    # )
    # print("Thêm thành công")
    print(user_mgr.check_user_name("vy"))