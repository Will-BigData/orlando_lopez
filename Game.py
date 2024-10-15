from Board import Board
from Player import Player
from Card import *
from random import randrange
from collections import defaultdict

import warnings

BOLD_START = "\033[1m"
RESET = "\033[0m"

warnings.filterwarnings("ignore", category=FutureWarning)
board = Board()
board.load_board()
board.load_cards()

running = True
i = 0
result = []



correct_num_players = False
while not correct_num_players:
    num_players = input("Choose the number of players (2-4) ")
    if num_players == "2" or num_players == "3" or num_players == "4":
        for i in range(int(num_players)):
            player_name = input(f"Enter the name for player {i + 1}: ")
            new_player = Player(player_name)
            new_player.tile = board.decision1
            new_player.board = board
            board.players.append(new_player)
        correct_num_players = True
    else:
        print("Error, input is invalid.")

players = board.players


def process_event(player: Player):
    print("-" * 20)
    if player.tile.type == "action":
    #     for testing
        # run = True
        # card = board.action_cards.pop()
        # while run:
        #     if card.interaction[0] != "s":
        #         card = board.action_cards.pop()
        #         continue
        #
        #     run = False
        card = board.action_cards.pop()
        player.action_cards.append(card)
        action_card_event(player, card)
    elif player.tile.type == "house":
        card1 = board.house_cards.pop()
        card2 = board.house_cards.pop()

        print(1)
        print(str(card1))
        print(2)
        print(str(card2))

        correct_selection = False
        while not correct_selection:

            selection = input(f"(1) {card1.name} (2) {card2.name} (3) None")

            if selection == "1":
                correct_selection = True
                player.houses.append(card1)
                player.money -= card1.price * 1000
                print(f"Purchased: {card1.name}")
            elif selection == "2":
                correct_selection = True
                player.houses.append(card2)
                player.money -= card2.price * 1000
                print(f"Purchased: {card2.name}")
            elif selection == "3":
                correct_selection = True
                print("No house purchased.")
            else:
                print("Error, select valid option.")

    elif player.tile.type == "spinner":
        num_selections = defaultdict(list)
        for p in players:
            correct_selection = False
            print(f"{p.name}'s turn")
            while not correct_selection:
                if p != player:
                    num = input("Pick your first number (1 - 10)")
                    if num.isdigit() and 1 <= int(num) <= 10:
                        correct_selection = True
                        num_selections[p].append(int(num))
                    else:
                        print("Error, enter a valid number between 1 and 10")

                else:
                    num1 = input("Pick your first number (1 - 10)")
                    num2 = input("Pick your second number (1 - 10)")
                    if num1.isdigit() and num2.isdigit() and 1 <= int(num1) <= 10 and 1 <= int(
                            num2) <= 10 and num1 != num2:
                        correct_selection = True
                        num_selections[p].append(int(num1))
                        num_selections[p].append(int(num2))
                    else:
                        print("Error, enter two different numbers between 1 and 10")

        hit = False
        while not hit:
            spin = randrange(1, 11)
            print(f"Spun a {spin}!")
            for p, nums in num_selections.items():
                for num in nums:
                    if num == spin:
                        p.money += 200000
                        print(f"{p.name} won $200,000!")
                        hit = True

    elif player.tile.type == "baby (b)":
        player.children.append("b")

    elif player.tile.type == "baby (g)":
        player.children.append("g")

    elif player.tile.type == "twins":
        player.children.append("g")
        player.children.append("b")

    elif player.tile.type == "pet":
        card = board.pet_cards.pop()
        action_card_event(player, card)
        player.pet_cards.append(card)

    elif player.tile.type == "payday":
        print("Get an extra $100,000!")

    elif player.tile.type == "decision2" or player.tile.type == "decision3" or player.tile.type == "decision4":
        player.move()
    elif player.tile.type == "get(300k)":
        player.money += 300000
        print("The bank pays you 300k!")
    elif player.tile.type == "get(200k)":
        player.money += 200000
        print("The bank pays you 200k!")
    elif player.tile.type == "pay(100k)":
        player.money += 100000
        print("The bank pays you 100k!")
    elif player.tile.type == "pay(100k)":
        player.money += 100000
        print("The bank pays you 100k!")

    elif player.tile.type == "S retirement":
        pass
    else:
        print(f"{player.tile.type} not handled")

    print("-" * 20)


def action_card_event(player: Player, card: ActionCard):
    print(f"{BOLD_START}{card.name}{RESET}")
    print(card.description)
    code = card.interaction[0]
    if code == "pb":
        transfer_amt = int(card.interaction[1]) * 1000
        player.money -= transfer_amt
        print(f"You paid the bank ${transfer_amt}!")
    elif code == "cb":
        transfer_amt = int(card.interaction[1]) * 1000
        player.money += transfer_amt
        print(f"The bank paid you ${transfer_amt}!")
    elif code == "cfe":
        transfer_amt = int(card.interaction[1]) * 1000
        for p in players:
            if p != player:
                p.money -= transfer_amt
                player.money += transfer_amt
        print(f"You collected ${transfer_amt} from everyone!")
    elif code == "rb":
        red_amt, black_amt = map(lambda x: int(x) * 1000, (card.interaction[1].split("|")))
        input(f"Enter anything to Spin; Red = ${red_amt}, Black = ${black_amt}")
        spin = randrange(1, 3)
        if spin == 1:
            print(f"Red! You receive ${red_amt}!")
            player.money += red_amt
        else:
            print(f"Black! You receive ${black_amt}!")
            player.money += black_amt
    elif code == "rbe":
        red_amt, black_amt = 50000, 100000
        print(f"Red = Pay ${red_amt} from the bank; Black = Pay the bank ${black_amt}")

        for p in players:
            print(f"{p.name}'s turn!")
            input(f"Enter anything to Spin! ")
            spin = randrange(1, 3)
            if spin == 1:
                print(f"Red! You receive ${red_amt}!")
                p.money += red_amt
            else:
                print(f"Black! You lost ${black_amt}!")
                p.money -= black_amt
    elif code == "fired":
        pass
    elif code == "laugh":
        pass

    elif code == "se":
        spinner_values = []
        x = card.interaction[1]
        range_list = x.split("|")
        for interval in range_list:
            y = interval.split("=")
            z = y[0].split("-")
            start = int(z[0])
            end = int(z[1])
            amt = int(y[1]) * 1000
            spinner_values.append([start, end, amt])

        for p in players:
            print(f"{p.name}'s turn to spin!")
            print(f"Spin      Collect From the Bank")
            for v in spinner_values:
                print(f"{v[0]}-{v[1]: <7} {v[2]}")
            input(f"Enter anything to Spin! ")
            spin = randrange(1, 11)
            print(f"You spun a {spin}!")
            for v in spinner_values:
                if v[0] <= spin <= v[1]:
                    p.money += v[2]
                    print(f"You receive ${v[2]}!")

    elif code == "pos":
        transfer_amt = int(card.interaction[1]) * 1000
        for j, p in enumerate(players):
            if p != player:
                print(f"({j}) {p.name}")

        correct_input = False
        while not correct_input:
            idx = input("Opponent? ")
            if (idx == "0" or idx == "1" or idx == "2" or idx == "3") and int(idx) < len(players):
                correct_input = True
                opponent = players[int(idx)]
                cur_player_spin = input(f"Enter anything to Spin! Winner receives ${transfer_amt}!")
                spin_result1 = randrange(1, 11)
                print(f"You spun a {spin_result1}!")

                print(f"{opponent.name}'s turn!")
                opp_player_spin = input(f"Enter anything to Spin! Winner receives ${transfer_amt}!")
                spin_result2 = randrange(1, 11)
                print(f"You spun a {spin_result2}!")

                if spin_result1 > spin_result2:
                    player.money += transfer_amt
                    print(f"{player.name} receives ${transfer_amt}!");

                elif spin_result1 < spin_result2:
                    opponent.money += transfer_amt
                    print(f"{opponent.name} receives ${transfer_amt}!");
                else:
                    player.money += transfer_amt
                    opponent.money += transfer_amt
                    print(f"Both receive ${transfer_amt}!");
            else:
                print("Error pick a valid player")

    elif code == "c10x":
        input(f"Enter anything to Spin! Collect 10k x your spin from the bank!")
        spin = randrange(1, 11)
        print(f"You spun a {spin} and received ${spin * 10000}!")
        player.money += spin * 10000

    elif code == "cp":
        transfer_amt = int(card.interaction[1]) * 1000

        for j, p in enumerate(players):
            if p != player:
                print(f"({j}) {p.name}")

        correct_input = False
        while not correct_input:
            idx = input("Opponent? ")
            if (idx == "0" or idx == "1" or idx == "2" or idx == "3") and int(idx) < len(players):
                correct_input = True
                opponent = players[int(idx)]
                opponent.money -= transfer_amt
                player.money += transfer_amt
                print(f"{player.name} took ${transfer_amt} from {opponent.name}")
            else:
                print("Error pick a valid player")

    elif code == "poc10x":
        for j, p in enumerate(players):
            if p != player:
                print(f"({j}) {p.name}")

        correct_input = False
        while not correct_input:
            idx = input("Opponent? ")
            if (idx == "0" or idx == "1" or idx == "2" or idx == "3") and int(idx) < len(players):
                correct_input = True
                opponent = players[int(idx)]
                input(f"Enter anything to Spin! Winner receives 10k x their spin!")
                spin_result1 = randrange(1, 11)
                print(f"You spun a {spin_result1}!")

                print(f"{opponent.name}'s turn!")
                input(f"Enter anything to Spin! Winner receives 10k x their spin!")
                spin_result2 = randrange(1, 11)
                print(f"You spun a {spin_result2}!")

                reward = max(spin_result1, spin_result2) * 10000

                if spin_result1 > spin_result2:
                    player.money += reward
                    print(f"{player.name} receives ${reward}!");

                elif spin_result1 < spin_result2:
                    opponent.money += reward
                    print(f"{opponent.name} receives ${reward}!");
                else:
                    player.money += reward
                    opponent.money += reward
                    print(f"Both receive ${reward}!");
            else:
                print("Error pick a valid player")

    elif code == "s":
        spinner_values = []
        x = card.interaction[1]
        range_list = x.split("|")
        for interval in range_list:
            y = interval.split("=")
            z = y[0].split("-")
            start = int(z[0])
            end = int(z[1])
            amt = int(y[1]) * 1000
            spinner_values.append([start, end, amt])

        print(f"Spin      Collect From the Bank")
        for v in spinner_values:
            print(f"{v[0]}-{v[1]: <7} {v[2]}")
        input(f"Enter anything to Spin! ")
        spin = randrange(1, 11)
        print(f"You spun a {spin}!")
        for v in spinner_values:
            if v[0] <= spin <= v[1]:
                player.money += v[2]
                print(f"You receive ${v[2]}!")


def pet_card_event(player: Player, card: PetCard):
    code = card.interaction[0]
    if code == "pb":
        transfer_amt = int(card.interaction[1]) * 1000
        player.money -= transfer_amt
    elif code == "cb":
        transfer_amt = int(card.interaction[1]) * 1000
        player.money += transfer_amt
    elif code == "pos":
        transfer_amt = int(card.interaction[1]) * 1000
        for j, p in enumerate(players):
            if p != player:
                print(f"({j}) {p.name}")

        correct_input = False
        while not correct_input:
            idx = input("Opponent? ")
            if (idx == "0" or idx == "1" or idx == "2" or idx == "3") and int(idx) < len(players):
                correct_input = True
                opponent = players[int(idx)]
                input(f"Enter anything to Spin! Winner receives ${transfer_amt}!")
                spin_result1 = randrange(1, 11)
                print(f"You spun a {spin_result1}!")

                print(f"{opponent.name}'s turn!")
                input(f"Enter anything to Spin! Winner receives ${transfer_amt}!")
                spin_result2 = randrange(1, 11)
                print(f"You spun a {spin_result2}!")

                if spin_result1 > spin_result2:
                    player.money += transfer_amt
                    print(f"{player.name} receives ${transfer_amt}!");

                elif spin_result1 < spin_result2:
                    opponent.money += transfer_amt
                    print(f"{opponent.name} receives ${transfer_amt}!");
                else:
                    player.money += transfer_amt
                    opponent.money += transfer_amt
                    print(f"Both receive ${transfer_amt}!");
            else:
                print("Error pick a valid player")

    elif code == "cb*p":
        transfer_amt = int(card.interaction[1]) * 1000 * len(player.pets)
        player.money += transfer_amt
    elif code == "pb*p":
        transfer_amt = int(card.interaction[1]) * 1000 * len(player.pets)
        player.money -= transfer_amt
    elif code == "cfe":
        transfer_amt = int(card.interaction[1]) * 1000
        for p in players:
            if p != player:
                p.money -= transfer_amt
                player.money += transfer_amt


def view_life(player: Player):
    print(f"Name: {player.name}")
    print(f"Money: ${player.money}")
    print("Career")
    print("-" * 20)
    print(str(player.career))
    print(f"Children: {len(player.children)}")
    print("Houses")
    print("-" * 20)
    for house in player.houses:
        print(str(house))
        print("-" * 20)
    print(f"Action Cards: {len(player.action_cards)}")
    print(f"Pet Cards: {len(player.pet_cards)}")
    # print(f"Loans: {player.loans}")


def export_game_stats():
    with open("game_stats.md", 'w') as file:
        for p, m in result:
            file.write(f"Name: {p.name}\n")
            file.write(f"Money: {p.money}\n")

            file.write("Career\n")
            file.write(str(p.career) + '\n')

            file.write(f"Children: {len(p.children)}\n")

            file.write("Houses\n")
            for house in p.houses:
                file.write(str(house) + '\n')

            file.write(f"Action Cards: {len(p.action_cards)}\n")
            file.write(f"Pet Cards: {len(p.pet_cards)}\n")
            # file.write(f"Loans: {p.loans}\n")
            file.write("\n")


while running:
    if not players:
        running = False
        for player in board.retired:
            player.money += len(player.action_cards) * 100000
            player.money += len(player.pet_cards) * 100000
            player.money += len(player.children) * 50000
            # player.money -= player.loans * 60000

            for house in player.houses:
                print(
                    f"Spin to sell {house.name}; Purchase Price = {house.price}k; Red = {house.sale_price_r}k; Black = {house.sale_price_b}k")
                input("Press enter to spin")
                spin = randrange(1, 3)
                if spin == 1:
                    print("You spun Red!")
                    player.money += house.sale_price_r * 1000
                else:
                    print("You spun Black!")
                    player.money += house.sale_price_b * 1000
            result.append([player, player.money])
        result.sort(key=lambda x: x[1], reverse=True)
        export_game_stats()

    if players:
        cur_player = players[i % len(players)]
    else:
        continue
    print(f"{cur_player.name}'s turn!")
    # 0 - first attempt, 1 - passed, 2 - error
    state = 0
    while state != 1:

        if i // len(players) == 0:
            cur_player.move()
        action = input("(1) Spin! (2) View Life (3) End Game ")
        if action == "1":

            spin_result = randrange(1, 11)
            print(f"You spun a {spin_result}!")
            cur_player.moves_left = spin_result
            board.move_player(cur_player)
            print(f"You landed on tile: {cur_player.tile.type}")
            process_event(cur_player)

            state = 1
        elif action == "2":
            view_life(cur_player)
        elif action == "3":
            running = False
            print("Ending Game")
            export_game_stats()
            state = 1
        else:
            state = 2
            print("Error, only the following inputs are acceptable: 1, 2, 3")

    i += 1
