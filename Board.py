from random import randrange, shuffle

from Tile import Tile
from Player import Player
import pandas as pd
from Card import *
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)


class Board:
    starting_tile = None
    routes = []
    decision1 = Tile("decision1")
    decision2 = Tile("decision2")
    decision3 = Tile("decision3")
    decision4 = Tile("decision4")
    union1 = Tile("action")
    union2 = Tile("action")
    union3 = Tile("action")
    house_cards = []
    fast_career_cards = []
    college_career_cards = []
    pet_cards = []
    action_cards = []
    players = []
    retired = []

    def load_new_tile(self, cur_tile, new_tile):
        cur_tile.next.append(new_tile)
        prev_tile = cur_tile
        cur_tile = cur_tile.next[-1]
        cur_tile.prev.append(prev_tile)
        return cur_tile

    def load_board(self):
        df = pd.read_csv("GameOfLifeMap.csv")
        num_cols = df.shape[1]
        cur_tile = None
        for i in range(num_cols):
            j = 0
            if i == 0 or i == 1:
                cur_tile = self.decision1
            elif i == 3 or i == 4:
                cur_tile = self.decision2
            elif i == 6 or i == 7:
                cur_tile = self.decision3
            elif i == 9 or i == 10:
                cur_tile = self.decision4
            elif i == 2:
                cur_tile = self.union1
            elif i == 5:
                cur_tile = self.union2
            elif i == 8:
                cur_tile = self.union3
            else:
                raise Exception("something broke while loading board")

            # cur_cell = df.iloc[0][i]
            while j < df.shape[0]:
                cur_cell = df.iloc[j][i]
                if pd.isna(cur_cell):
                    break

                cur_tile = self.load_new_tile(cur_tile, Tile(cur_cell))

                j += 1

            if i == 0 or i == 1:
                # cur_tile.next.append(self.union1)
                self.load_new_tile(cur_tile, self.union1)
            elif i == 3 or i == 4:
                # cur_tile.next.append(self.union2)
                self.load_new_tile(cur_tile, self.union2)
            elif i == 6 or i == 7:
                # cur_tile.next.append(self.union3)
                self.load_new_tile(cur_tile, self.union3)
            elif i == 2:
                self.load_new_tile(cur_tile, self.decision2)
            elif i == 5:
                self.load_new_tile(cur_tile, self.decision3)
            elif i == 8:
                self.load_new_tile(cur_tile, self.decision4)
            elif i == 9 or i == 10:
                pass
            else:
                raise Exception("something broke while loading board")

    def check_board(self):
        cur_tile = self.decision1
        while cur_tile and len(cur_tile.next) > 0:
            print(f"{cur_tile.type} -> ", end="")
            cur_tile = cur_tile.next[0]
        print(cur_tile.type)

    def move_player(self, player: Player):
        for i in range(player.moves_left):
            player.move()
            player.moves_left -= 1

            if player.tile.type == "get married":
                red_amt, black_amt = 50000, 100000
                print(f"You're getting married, Time for wedding gifts!")
                print(f"Red = ${red_amt}; Black = ${black_amt}")
                for p in self.players:
                    if p == player:
                        continue
                    print(f"{p.name}'s turn to spin for gifts!")
                    input(f"Enter anything to Spin!")
                    spin = randrange(1, 3)
                    if spin == 1:
                        print(f"Red! You give {player.name} ${red_amt}!")
                        player.money += red_amt
                        p.money -= red_amt

                    else:
                        print(f"Black! You give {player.name} ${black_amt}!")
                        player.money += black_amt
                        p.money -= black_amt

                player.moves_left = 0
                print(f"Back to {player.name}!")
                input("Press enter to spin again!")
                spin = randrange(1, 11)
                player.moves_left = spin
                self.move_player(player)
            elif player.tile.type == "graduation":
                card1 = self.college_career_cards.pop()
                card2 = self.college_career_cards.pop()

                print(1)
                print(str(card1))
                print(2)
                print(str(card2))

                correct_selection = False
                while not correct_selection:
                    selection = input(f"(1) {card1.name} (2) {card2.name} ")
                    if selection == "1":
                        correct_selection = True
                        player.career = card1
                        print(f"Selected career:  {card1.name}")
                    elif selection == "2":
                        correct_selection = True
                        player.career = card2
                        print(f"Selected career:  {card2.name}")
                    else:
                        print("Error, select valid option.")
                player.moves_left = 0
                input("Press enter to spin again!")
                spin = randrange(1, 11)
                player.moves_left = spin
                self.move_player(player)

            elif player.tile.type == "S babyspin":
                print("Spin for Babies")
                print("1-3: 0 babies; 4-6: 1 baby; 7-8: twins; 9-10: triplets")
                input("press enter to spin!")
                spin = randrange(1, 11)
                if 1 <= spin <= 3:
                    print("No Babies!")
                elif 4 <= spin <= 6:
                    print("One Baby!")
                    player.children.append("g")
                elif 7 <= spin <= 8:
                    print("Twins!")
                    player.children.append("g")
                    player.children.append("b")
                else:
                    player.children.append("g")
                    player.children.append("g")
                    player.children.append("g")
                    print("Triplets!")

                player.moves_left = 0
                input("Press enter to spin again!")
                spin = randrange(1, 11)
                player.moves_left = spin
                self.move_player(player)
            elif player.tile.type == "payday":
                player.money += player.career.salary * 1000
                print("You got paid!")
            elif player.tile.type == "S retirement":
                if player not in self.retired:
                    self.retired.append(player)
                if player in self.players:
                    self.players.remove(player)

                if len(self.retired) == 1:
                    player.money += 400000
                    print("You received $400,000 for retiring first!")
                elif len(self.retired) == 2:
                    player.money += 300000
                    print("You received $300,000 for retiring second!")
                elif len(self.retired) == 3:
                    player.money += 200000
                    print("You received $200,000 for retiring third!")
                elif len(self.retired) == 4:
                    player.money += 100000
                    print("You received $100,000 for retiring fourth!")
                else:
                    print("something broke at retirement")
                if not self.players:
                    break

    def load_cards(self):
        df = pd.read_csv("GameOfLifeCards.csv")
        num_cols = df.shape[1]
        for i in range(num_cols):
            cur_cell = df.iloc[0][i]
            j = 0
            while j < df.shape[0]:
                cur_cell = df.iloc[j][i]
                if pd.isna(cur_cell):
                    break

                cell_info = cur_cell.split(",")
                if i == 0:
                    house_card = HouseCard(cell_info[0], int(cell_info[1]), int(cell_info[2]), int(cell_info[3]))
                    self.house_cards.append(house_card)
                elif i == 1:
                    fast_career_card = FastCareerCard(cell_info[0], int(cell_info[1]), cell_info[2])
                    self.fast_career_cards.append(fast_career_card)

                elif i == 2:
                    college_career_card = CollegeCareerCard(cell_info[0], int(cell_info[1]), cell_info[2])
                    self.college_career_cards.append(college_career_card)
                elif i == 3:
                    pet_card = PetCard(cell_info[0], cell_info[1], cell_info[2].split(":"))
                    self.pet_cards.append(pet_card)
                elif i == 4:
                    action_card = ActionCard(cell_info[0], cell_info[1], cell_info[2].split(":"))
                    self.action_cards.append(action_card)

                j += 1
        shuffle(self.action_cards)
        shuffle(self.fast_career_cards)
        shuffle(self.college_career_cards)
        shuffle(self.house_cards)
        shuffle(self.pet_cards)

