from db.db import db

class DeckManager():
    def __init__(self):
        self.__my_db = db()
        self.deck_df = None
        self.get_deck_db()

    def get_deck_db(self):
        '''Lấy thông tin deck trong db'''
        query = "SELECT * FROM `fc`.`decks`;"
        self.deck_df = self.__my_db.query(query)

    def add_deck_db(self, deck_name: str):
        '''Thêm deck vào db'''
        query = "INSERT INTO `fc`.`decks`(deck_name) VALUES (%s, %s);"
        param = (deck_name, 1)
        self.__my_db.dml_ddl_operator(query, param)
        self.get_deck_db()

    def delete_deck_db(self, deck_id: int):
        '''Xóa db khỏi db từ dekc_id'''
        # Xóa word
        query = "DELETE FROM `fc`.`words` where word_deck_id = %s;"
        param = (deck_id, )
        self.__my_db.dml_ddl_operator(query= query, params= param)
        print(f"Xóa các word của deck {deck_id} thành công")

        # Xóa deck
        query = "DELETE FROM `fc`.`decks` where deck_id = %s;"
        self.__my_db.dml_ddl_operator(query=query, params= param)
        print(f"Xóa deck {deck_id} thành công")
        self.get_deck_db()

if __name__ == "__main__":
    deck_manager = DeckManager()
    deck_manager.get_deck_db()
    print(deck_manager.deck_df)
    deck_manager.delete_deck_db(11)
    print("DS Deck mới:")
    print(deck_manager.deck_df)
