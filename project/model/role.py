class Role:
    """Lớp mô tả vai trò người dùng."""
    def __init__(self, role_id=None, role_name=None):
        self._role_id = role_id
        self._role_name = role_name

    def get_role_id(self): return self._role_id
    def set_role_id(self, role_id): self._role_id = role_id

    def get_role_name(self): return self._role_name
    def set_role_name(self, role_name): self._role_name = role_name

    def __repr__(self):
        return f"Role(ID={self._role_id}, Name='{self._role_name}')"
