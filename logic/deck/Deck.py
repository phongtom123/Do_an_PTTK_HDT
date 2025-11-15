from db.db import db
from logic.deck.Card import Card

class Deck():
    def __init__(self, deck_id, deck_name):
        self.__my_db = db()
        self._deck_id = deck_id
        self._deck_name = deck_name
        self._df = None
        self.card_list = [] # Đây là card list chứa card thuộc về deck

        self.fetch_db()
    
    def __repr__(self):
        return f"Deck id: {self._deck_id}. Deck name: {self._deck_name}"
    
    def get_deck_id(self):
        return self._deck_id
    def get_deck_name(self):
        return self._deck_name
    
    def count_total_card(self):
        '''Lấy tổng số card trong deck'''
        return len(self.card_list)
    
    def count_known_card(self):
        '''Lấy tổng số card dã biết trong deck'''
        cnt = 0
        for card in self.card_list:
            if card.get_card_status == 1:
                cnt += 1
        return cnt

    def count_unknown_card(self):
        '''Lấy tổng số card chưa biết trong deck'''
        cnt = 0
        for card in self.card_list:
            if card.get_card_status == 0:
                cnt += 1
        return cnt

    def add_card(self, card_front, card_back):
        """Tạo class mới trong db và trong list. Trả về true nếu thành công"""
        card_status = 0 # Card mới tạo mặc định là ko nhớ
        card_deck_id = self.get_deck_id()
        # Lưu vào db
        query = \
        """insert into fc_cards(card_fe, card_be, card_status, card_deck_id) values
            (%s, %s, %s, %s)"""
        params = (card_front, card_back, card_status, card_deck_id)
        try:
            card_id = self.__my_db.dml_ddl_operator(query, params)
        except Exception as err:
            print(f"Có lỗi xảy ra khi thêm card vào deck {self._deck_id}. Lỗi {err}")
            return False
        # Đưa vào list
        new_card = Card(
            card_id= card_id,
            front_content= card_front,
            back_content= card_back,
            card_status= card_status
        )
        self.card_list.append(new_card)
        return True
    
    def find_card(self,card_id):
        '''Tìm card trong db từ id. Trả về đối tượng Card nếu tìm thấy, Nếu không trả về False'''
        for card in self.card_list:
            if card.get_card_id() == card_id:
                return card
        return False
            
    def filter_card(self, status):
        '''Loc ra cac card theo status. Lưu đối tượng vào 1 list'''
        flag_ls = []
        for card in self.card_list:
            if card.get_card_status() == status:
                flag_ls.append(card)
        return flag_ls
    
    def fetch_db(self):
        ''' Lấy dữ liêu card từ db'''
        query = "select * from fc_cards where card_deck_id = %s"
        params = (self._deck_id,)
        try:
            self._df = self.__my_db.query(query, params)
        except Exception as err:
            print(f"Có lỗi xảy ra khi fetch Deck. Lỗi {err}")

        # Lưu vào card_list
        for i, row in self._df.iterrows():
            card = Card(
                card_id = row["card_id"],
                front_content= row["card_fe"],
                back_content= row["card_be"],
                card_status= row["card_status"]
            )
            self.card_list.append(card)


if __name__ == "__main__":
    my_deck = Deck(3, "Hobbies Deck")
    # for card in my_deck.card_list:
    #     print(card)

    print(my_deck._df)