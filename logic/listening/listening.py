from logic.test.Test import Test

class Listening(Test):
    def __init__(self, listening_id, listening_content, listening_audio):
        super().__init__(test_id=listening_id, test_content=listening_content)
        self._listening_id = listening_id
        self._listening_content = listening_content
        self._listening_audio = listening_audio

    def get_content(self):
        return self._listening_content

    def get_audio(self):
        return self._listening_audio

    def __repr__(self):
        return f"Listening(id={self._listening_id})"
