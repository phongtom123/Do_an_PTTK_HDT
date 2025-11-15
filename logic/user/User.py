class User():
    def __init__(
            self, user_name, user_password, 
            user_rank, user_email, user_status, user_role_id, user_id = None):
        
        self._user_id = user_id
        self._user_name = user_name
        self._user_password = user_password
        self._user_rank = user_rank
        self._user_email = user_email
        self._user_status = user_status
        self._user_role_id = user_role_id
    # Getter
    def get_user_role_id(self):
        return self._user_role_id

    def get_user_id(self):
        return self._user_id

    def get_user_email(self):
        return self._user_email
    
    def get_user_name(self):
        return self._user_name

    def get_user_password(self):
        return self._user_password

    def get_user_rank(self):
        return self._user_rank

    def get_created_at(self):
        return self._created_at

    def get_user_status(self):
        return self._user_status

    # setter

    def set_user_name(self, user_name: str):
        self._user_name = user_name

    def set_user_password(self, user_password: str):
        self._user_password = user_password

    def set_user_rank(self, user_rank: int):
        self._user_rank = user_rank

    def set_user_status(self, user_status: int):
        self._user_status = user_status

    def __repr__(self):
        return (
        f"User("
        f"user_id={self._user_id}, "
        f"user_name='{self._user_name}', "
        f"user_password='***', "
        f"user_rank={self._user_rank}, "
        f"user_email={self._user_email}, "
        f"user_status={self._user_status}, "
        f"user_role= {self._user_role_id}"
    )

