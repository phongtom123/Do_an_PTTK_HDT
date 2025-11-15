from logic.test.Test import Test

class Reading(Test):
    def __init__(self, reading_id, reading_content):
        super().__init__(test_id=reading_id, test_content=reading_content)
        self._reading_id = reading_id
        self._reading_content = reading_content

    def get_content(self):
        return self._reading_content

    def __repr__(self):
        return f"Reading(id={self._reading_id})"
