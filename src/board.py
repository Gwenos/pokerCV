class Card : 
    def __init__(self, rank_, suit_, contour_): 
        self.rank = "10" if rank_=="0" else rank_ 
        self.suit = suit_ 
        self.contour = contour_ 
        
    def __eq__(self, other_) : 
        return self.rank==other_.rank and self.suit==other_.suit 
    
    def __hash__(self): 
        return hash((self.rank, self.suit)) 
    
    def __str__(self): 
        rank_dict = { 
            "A":"As", 
            "2":"2", 
            "3":"3", 
            "4":"4", 
            "5":"5", 
            "6":"6", 
            "7":"7", 
            "8":"8", 
            "9":"9", 
            "10":"10", 
            "J":"Valet", 
            "Q":"Reine", 
            "K":"Roi", 
        } 
        suit_dict = { 
            "H":"Coeur", 
            "D":"Carreau", 
            "S":"Pique", 
            "C":"Trefle", 
        }

        return f"{rank_dict[self.rank]} de {suit_dict[self.suit]}" 
        
    def get_rank(self) : 
        rank_dict = { 
            "2":2, 
            "3":3, 
            "4":4, 
            "5":5, 
            "6":6, 
            "7":7, 
            "8":8, 
            "9":9, 
            "10":10, 
            "J":11, 
            "Q":12, 
            "K":13, 
            "A":14, 
        }
        return rank_dict[self.rank]

class Board : 
    def __init__(self): 
        self.table_cards = [] 
        self.player_cards = [] 
        
    def __str__(self): 
        return f"{[str(c) for c in self.table_cards]}\n{[str(c) for c in self.player_cards]}" 
    
    def all_cards(self): 
        return self.table_cards + self.player_cards 
    
    def add_table_card(self, card_) : 
        self.table_cards.append(card_) 
        
    def add_player_card(self, card_) : 
        self.player_cards.append(card_) 
        
    def count_rank(self, card_): 
        cards = list(filter(lambda card : card.get_rank()==card_.get_rank(), self.all_cards()))
        return len(cards), cards
            
    def count_suit(self, card_): 
        cards = list(filter(lambda card : card.suit==card_.suit, self.all_cards()))
        return len(cards), cards
    
    def best_hand(self) : 
        flag, cards = self.is_quinte_flush_royal() 
        if flag : return "Quinte flush royal", cards 
        flag, cards = self.is_quinte_flush() 
        if flag : return "Quinte flush", cards 
        flag, cards = self.is_carre() 
        if flag : return "Carre", cards 
        flag, cards = self.is_full() 
        if flag : return "Full", cards 
        flag, cards = self.is_color() 
        if flag : return "Couleur", cards 
        flag, cards = self.is_quinte() 
        if flag : return "Quinte", cards 
        flag, cards = self.is_brelan()
        if flag : return "Brelan", cards 
        flag, cards = self.is_double_pair() 
        if flag : return "Double paire", cards 
        flag, cards = self.is_pair() 
        if flag : return "Paire", cards 
        _, cards = self.is_high_card() 
        return "High card", cards 
    
    def is_high_card(self) : 
        cards = sorted(self.player_cards, key=Card.get_rank) 
        return True, [cards[-1]] 
    
    def is_pair(self) : 
        distrib = map(self.count_rank, self.all_cards()) 
        distrib = dict(distrib) 
        return (True, distrib[2] ) if 2 in distrib else (False, []) 
    
    def is_double_pair(self) : 
        cpt_pair = 0 
        cards = [] 
        visited = [] 
        for card in self.all_cards() : 
            cpt_rank, c = self.count_rank(card) 
            if cpt_rank == 2 and card not in visited: 
                cpt_pair += 1 
                cards = cards + c 
            visited.append(card) 
        return cpt_pair >= 2, cards 
        
    def is_brelan(self): 
        distrib = map(self.count_rank, self.all_cards()) 
        distrib = dict(distrib) 
        return (True, distrib[3] ) if 3 in distrib else (False, []) 
        
    def is_quinte(self, cards_=None): 
        cards = sorted(self.all_cards(), key=Card.get_rank) if cards_ == None else sorted(cards_, key=Card.get_rank)
        cpt = 0 
        cards_returned = [] 
        for i in range(len(cards)-1) : 
            if cards[i].get_rank()+1 == cards[i+1].get_rank() : 
                cpt += 1 
                cards_returned.append(cards[i]) 
                if cpt == 4: 
                    cards_returned.append(cards[i+1]) 
                    return True, cards_returned 
            else : 
                cpt = 0 
                cards_returned = [] 
        return False, [] 
            
    def is_color(self): 
        distrib = map(self.count_suit, self.all_cards())
        distrib = dict(distrib) 
        return (True, distrib[5]) if 5 in distrib else (False, []) 
            
    def is_full(self): 
        distrib = map(self.count_rank, self.all_cards()) 
        distrib = dict(distrib) 
        return (True, distrib[3]+distrib[2]) if 3 in distrib and 2 in distrib else (False,[])
            
    def is_carre(self): 
        distrib = map(self.count_rank, self.all_cards()) 
        distrib = dict(distrib) 
        return (True, distrib[4]) if 4 in distrib else (False, [])
            
    def is_quinte_flush(self): 
        color, color_cards = self.is_color()
        quinte, _ = self.is_quinte(cards_=color_cards)

        if quinte and color :
            return True, color_cards
        return False, []
    
    def is_quinte_flush_royal(self): 
        color, color_cards = self.is_color()
        quinte, _ = self.is_quinte(cards_=color_cards)

        if not(quinte or color) :
            return False, []
        
        ranks = list(map(lambda card:card.get_rank(), color_cards))
        royal_ranks = [10, 11, 12, 13, 14]
        for royal_rank in royal_ranks :
            if royal_rank not in ranks :
                return False, []
        
        return True, color_cards
