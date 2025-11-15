from db.db import db
from logic.listening.listening import Listening

class ListeningManager:
    def __init__(self):
        self.db = db()

    def get_by_test_id(self, test_id):
        df = self.db.query(
            "SELECT listening_test_id, listening_content, listening_audio "
            "FROM listenings WHERE listening_test_id = %s",
            (int(test_id),)
        )

        result = []
        for _, row in df.iterrows():
            result.append(
                Listening(
                    listening_id=row["listening_test_id"],
                    listening_content=row["listening_content"],
                    listening_audio=row["listening_audio"]
                )
            )
        return result
