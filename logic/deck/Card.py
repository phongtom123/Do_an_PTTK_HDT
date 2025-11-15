class Card():
    def __init__(
            self, 
            front_content, 
            back_content, 
            card_status,
            card_id = None):
            
        self._card_id = card_id
        self._front_content = front_content
        self._back_content = back_content
        self._card_status = card_status

    def get_card_id(self):
        return self._card_id

    def set_card_id(self, value):
        self._card_id = value

    def get_front_content(self):
        return self._front_content

    def set_front_content(self, value):
        self._front_content = value

    def get_back_content(self):
        return self._back_content

    def set_back_content(self, value):
        self._back_content = value

    def get_card_status(self):
        return self._card_status

    def set_card_status(self, value):
        self._card_status = value

    def __repr__(self):
        return (f"Card("
            f"card_id={self._card_id!r}, "
            f"front_content={self._front_content!r}, "
            f"back_content={self._back_content!r}, "
            f"card_status={self._card_status!r})")