class User:
    """Lớp mô tả người dùng trong hệ thống BLEU."""

    def __init__(self, user_id=None, user_name=None, user_password=None,
                 user_role_id=None, user_rank=0, user_level=1, user_status=1):
        self._user_id = user_id
        self._user_name = user_name
        self._user_password = user_password
        self._user_role_id = user_role_id
        self._user_rank = user_rank
        self._user_level = user_level
        self._user_status = user_status

    def get_user_id(self): return self._user_id
    def set_user_id(self, user_id): self._user_id = user_id

    def get_user_name(self): return self._user_name
    def set_user_name(self, name): self._user_name = name

    def get_user_password(self): return self._user_password
    def set_user_password(self, password): self._user_password = password

    def get_user_role_id(self): return self._user_role_id
    def set_user_role_id(self, role_id): self._user_role_id = role_id

    def get_user_rank(self): return self._user_rank
    def set_user_rank(self, rank): self._user_rank = rank

    def get_user_level(self): return self._user_level
    def set_user_level(self, level): self._user_level = level

    def get_user_status(self): return self._user_status
    def set_user_status(self, status): self._user_status = status

    def __repr__(self):
        return f"User(ID={self._user_id}, Name='{self._user_name}', Role={self._user_role_id}, Rank={self._user_rank}, Level={self._user_level}, Status={self._user_status})"
