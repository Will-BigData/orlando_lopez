from random import randrange, shuffle

from Card import FastCareerCard
from Tile import Tile


class Player:
    name = ""
    money = 200000
    pets = []
    children = []
    houses = []
    action_cards = []
    pet_cards = []
    career = None
    tile = None
    moves_left = 0
    board = None
    # loans = 0

    def __init__(self, name=""):
        self.name = name
        self.money = 200000
        self.pets = []
        self.children = []
        self.houses = []
        self.action_cards = []
        self.pet_cards = []
        self.career = None
        self.tile = None
        self.moves_left = 0
        self.board = None
        # self.loans = 0

    # You can add methods here to perform actions related to the player



    def move(self):
        waiting_for_valid_input = True

        while waiting_for_valid_input:
            if len(self.tile.next) == 1:
                self.tile = self.tile.next[0]
                waiting_for_valid_input = False
            elif len(self.tile.next) == 2:
                path = ""
                if self.tile.type == "decision1":
                    print("Must pay $100,000 for College tuition")
                    path = input("(1) Career Path (2) College Path ")
                elif self.tile.type == "decision2":
                    print("Must pay $100,000 for Night School tuition")
                    path = input("(1) Life Path (2) Night School ")
                elif self.tile.type == "decision3":
                    path = input("(1) Family Path (2) Life Path ")
                elif self.tile.type == "decision4":
                    path = input("(1) Risky Road (2) Safe Route ")

                else:
                    print("something broke in player.move()")
                if path == "1":
                    # Career Path
                    if self.tile.type == "decision1":
                        card1 = self.board.fast_career_cards.pop()
                        card2 = self.board.fast_career_cards.pop()

                        print(1)
                        print(str(card1))
                        print(2)
                        print(str(card2))

                        correct_selection = False
                        while not correct_selection:
                            selection = input(f"(1) {card1.name} (2) {card2.name}")
                            if selection == "1":
                                correct_selection = True
                                self.board.fast_career_cards.append(card2)
                                shuffle(self.board.fast_career_cards)

                                self.career = card1
                                print(f"Selected career:  {card1.name}")
                            elif selection == "2":
                                correct_selection = True
                                self.board.fast_career_cards.append(card1)
                                shuffle(self.board.fast_career_cards)
                                self.career = card2
                                print(f"Selected career:  {card2.name}")

                            else:
                                print("Error, select valid option.")

                    # Life Path
                    if self.tile.type == "decision2":
                        self.moves_left = 0
                        input("Press enter to spin again!")
                        spin = randrange(1, 11)
                        self.moves_left = spin

                    self.moves_left = 0
                    if self.tile.type != "decision1":
                        input("Press enter to spin again!")
                        spin = randrange(1, 11)
                        print(f"You spun a {spin}!")
                        self.moves_left = spin - 1
                    self.tile = self.tile.next[0]
                    waiting_for_valid_input = False
                elif path == "2":
                    # College Path
                    if self.tile.type == "decision1":
                        self.money -= 100000

                    # Night School
                    if self.tile.type == "decision2":
                        card1 = self.board.college_career_cards.pop()

                        print(1)
                        print(str(card1))

                        correct_selection = False
                        while not correct_selection:
                            selection = input(f"(1) {card1.name} (2) Keep current career ")
                            if selection == "1":
                                correct_selection = True
                                if type(self.career) == FastCareerCard:
                                    self.board.fast_career_cards.append(self.career)
                                    shuffle(self.board.fast_career_cards)
                                else:
                                    self.board.college_career_cards.append(self.career)
                                    shuffle(self.board.college_career_cards)

                                self.career = card1
                                print(f"Selected career:  {card1.name}")
                            elif selection == "2":
                                correct_selection = True
                                self.board.college_career_cards.append(card1)
                                shuffle(self.board.college_career_cards)
                                print(f"Stayed as a {self.career.name}")
                            else:
                                print("Error, select valid option.")
                        self.money -= 100000
                    if self.tile.type != "decision1":
                        self.moves_left = 0
                        input("Press enter to spin again!")
                        spin = randrange(1, 11)
                        print(f"You spun a {spin}!")
                        self.moves_left = spin - 1
                    self.tile = self.tile.next[1]
                    waiting_for_valid_input = False
                else:
                    print("Error, only the following inputs are acceptable: 1, 2, 3")

            else:
                waiting_for_valid_input = False
                print("SOMETHING BROKE!")
