BOLD_START = "\033[1m"
RESET = "\033[0m"

class Card:
    name = ""


class HouseCard(Card):
    def __init__(self, name, price, sale_price_r, sale_price_b):
        self.name = name
        self.price = price
        self.sale_price_r = sale_price_r
        self.sale_price_b = sale_price_b

    def __str__(self):
        return (f"{self.name}\n"
                f"Price: ${self.price}k\n"
                f"Red Sale Price: ${self.sale_price_r}k\n"
                f"Black Sale Price: ${self.sale_price_b}k")
    price = -1
    sale_price_r = -1
    sale_price_b = -1


class FastCareerCard(Card):
    def __init__(self, name, salary, bonus_number):
        self.name = name
        self.salary = salary
        self.bonus_number = bonus_number

    def __str__(self):
        return (f"{self.name}\n"
                f"Salary: ${self.salary}k\n"
                f"Bonus Number: {self.bonus_number}")
    salary = -1
    bonus_number = -1


class CollegeCareerCard(Card):
    def __init__(self, name, salary, bonus_number):
        self.name = name
        self.salary = salary
        self.bonus_number = bonus_number

    def __str__(self):
        return (f"{self.name}\n"
                f"Salary: ${self.salary}k\n"
                f"Bonus Number: {self.bonus_number}")
    salary = -1
    bonus_number = -1


class PetCard(Card):
    def __init__(self, name, description, interaction):
        self.name = name
        self.description = description
        self.interaction = interaction

    description = ""
    interaction = []


class ActionCard(Card):
    def __init__(self, name, description, interaction):
        self.name = name
        self.description = description
        self.interaction = interaction
    description = ""
    interaction = []

