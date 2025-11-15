from db.db import db
from .Deck import Deck

class DeckManager():
    def __init__(self, user_id):
        self.__my_db = db()
        self._df = None
        self._user_id = int(user_id)
        self.deck_list = []
        self.fetch_db()

    def is_deck_list_empty(self):
        return len(self.deck_list) == 0
    
    def fetch_db(self):
        # Lưu vào df
        query = "select * from fc_decks where deck_user_id = %s"
        params = (self._user_id,)
        try:
            self._df = self.__my_db.query(query, params)
        except Exception as err:
            print(f"Đã có lỗi xảy ra fetch fc_decks. Lỗi {err}")
        
        # Lưu vào deck_list
        for i, row in self._df.iterrows():
            deck = Deck(row["deck_id"], row["deck_name"])
            self.deck_list.append(deck)
    
    def add_deck(self, deck_name):
        '''Thêm deck vào db và deck_list. Trả về true nếu thêm deck thành công'''
        query = "insert into fc_decks(deck_name, deck_user_id) values (%s, %s)"
        params = (deck_name, self._user_id)
        try:
            deck_id = self.__my_db.dml_ddl_operator(query, params)
            new_deck = Deck(
                deck_id = deck_id,
                deck_name= deck_name
            )
            self.deck_list.append(new_deck)
            return True
        except Exception as err:
            print(f"Có lỗi xảy ra khi add_deck. Lỗi {err}")
            return False
        
    def find_deck(self, deck_id: int):
        """Tìm deck theo id. nếu có trả về deck, nếu không trả về false"""
        for deck in self.deck_list:
            if deck.get_deck_id() == deck_id:
                return deck
        return False
    
    def delete_deck(self, deck_id: int):
        '''Xóa deck khỏi deck_list và db nếu có'''
        # Xóa khỏi deck_list
        delete_deck = self.find_deck(deck_id)
        if delete_deck != False:
            self.deck_list.remove(delete_deck)
            
            # Xóa khỏi db
            query = "delete from fc_cards where card_deck_id = %s"
            params = (deck_id, )
            try:
                self.__my_db.dml_ddl_operator(query, params) # Xóa từ của deck
                query = "delete from fc_decks where deck_id = %s"
                self.__my_db.dml_ddl_operator(query, params) # Xóa deck
            except Exception as err:
                print(f"Có lỗi xảy ra khi xóa deck. Lỗi {err}")

if __name__ == "__main__":
    print("Đã test")