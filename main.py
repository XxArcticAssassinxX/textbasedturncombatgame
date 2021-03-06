"""
File:    main.py
Author1:  Arctis   (https://github.com/XxArcticAssassinxX)
Author2:  M0RGANZ  (https://github.com/morganzwest) [https://morganz.co.uk]
Version 0.2.47
"""

import random
import math
import time
import sys
import json
from colors import color

dev = False
version = "0.2.52"

# Get Data
with open("loaddata.json", "r") as file:
    character_load = json.load(file)
# Get Data


def print_type(array, speed=0.02):
    """
    This function takes an array of values then flushes each
    character "one by one" outputs them instead of default print()

    :param array: Array of values to be printed
    :param speed: The partition between each character being printed
    :return: None
    """

    a = []
    for node in array:
        a.append(str(node))

    a.append("\n")
    if not dev:  # Within the PyCharm Environment outputting characters at this speed can cause issues

        for string in a:
            for char in string:
                time.sleep(speed)
                sys.stdout.write(char)
                sys.stdout.flush()

    else:
        print(a)


# This will store the BOT and PLAYER so they are easily accessible
characters = []


class Character:
    def __init__(self, health: int, bot=False):
        self.hp = health
        self.heal_cooldown = 1
        self.bot = bot
        self.opponent = None

        # Assign the type of opponent
        if self.bot:  # BOT

            try:
                self.type = character_load[random.randint(1, len(character_load))]
            except IndexError:
                self.type = character_load[random.randint(1, len(character_load))]

            self.name = self.type["name"]
            self.actions = self.type["actions"]
            self.damage = self.type["damage"]
            self.default_cooldown = self.type["def-cool"]

        else:  # PLAYER
            self.type = None
            self.actions = "strikes"
            self.damage = [50, 100]
            self.default_cooldown = 8
        # Assign the type of opponent

    def set_op(self):
        """
        This function assigns the other instance as the opponent
        :return: None
        """

        if self.bot:
            self.opponent = characters[0]
        else:
            self.opponent = characters[1]

    def __check_health(self):
        if self.hp <= 0:
            return False
        else:
            return True

    def turn(self):
        """
        This function will be run every single loop
        It checks which move the player wants to play
        and then runs the other functions within the class

        :return: Sub Formative's
        """
        if self.__check_health():  # Null Move Check
            if self.bot:
                c = random.randint(1, 2)
                if c == 2:
                    self.heal_check()
                else:
                    self.attack()
            else:
                print_type(["Attack(A) or heal(H): "])
                answer = input("> ")
                # answer.lower() just so the player cannot break the script as easily
                if answer.lower() == "a":
                    self.attack()
                elif answer.lower() == "h":
                    self.heal_check()
                elif answer.lower() == "version":
                    print_type([f"Version: {version}"])
                else:
                    print_type([color.place("red"), "Enter 'a' or 'h'.", color.place("reset")])
                    self.turn()

    def attack(self):
        """
        This function conditions all the damage onto the other instance
        :return: None
        """
        self.heal_cooldown -= 1
        self.opponent.heal_cooldown -= 1
        player_dmg = random.randint(self.damage[0], self.damage[1])
        player_critical_chance = random.randint(1, 3)
        player_critical_int = random.randint(1, 3)
        player_net_dmg = random.randint(120, 200)

        if player_critical_int == player_critical_chance:

            player_net_dmg = math.ceil(player_net_dmg)
            self.opponent.hp -= player_net_dmg

            # Different outputs depending if it is the BOT instance
            if not self.bot:
                print_type(["You land a critical hit, dealing ", player_net_dmg,
                            f" damage to the {self.opponent.name}. The enemy has ", self.opponent.hp,
                            " health remaining."])
            else:
                print_type([f"{self.name} hit a critical hit, dealing ", player_net_dmg, " damage to you. You have ",
                            self.opponent.hp, " health remaining."])
        else:
            self.opponent.hp -= player_dmg
            if not self.bot:
                print_type(["You strike the enemy, dealing ", player_dmg, f" damage. The {self.opponent.name} has ",
                            self.opponent.hp, " health remaining."])
            else:
                print_type([f"The {self.opponent.name} strikes, dealing ", player_dmg, " damage. You now have ",
                            self.opponent.hp, " health remaining."])

    def heal_check(self):
        """
        Check if the cooldown is at zero to allow for healing
        :return: None
        """
        if self.heal_cooldown > 0:
            if not self.bot:
                print_type(["You cannot heal for another ", self.heal_cooldown, " turns."])
                self.turn()
            else:
                self.attack()
        else:
            self.heal()

    def heal(self):
        """
        Reset the cooldown to default and output the random health change
        :return: None
        """
        self.heal_cooldown = self.default_cooldown
        self.opponent.heal_cooldown -= 1
        c = random.randint(100, 200)
        self.hp += c
        if self.hp > 1000:
            self.hp = 1000

        # Different output depending on if the instance is a BOT
        if not self.bot:
            print_type(["Healed ", c, " health."])
        else:
            print_type([f"{self.name} Healed ", c, " health"])

    def death(self):
        if not self.bot:
            print_type(["You DIED"])
        else:
            print_type([f"YOU KILLED THE {self.name.upper()}"])


def reset():
    """
    Setup the game
    :return: None
    """
    player = Character(1000)
    bot = Character(1000, bot=True)
    characters.append(player)
    characters.append(bot)

    player.set_op()
    bot.set_op()

    run = True
    print_type(["You have found a ", bot.name])
    while run:

        if dev:
            for c in characters:
                print(c.bot, c.hp, c.heal_cooldown)

        # Check the array of characters in-case one of them is dead
        for character in characters:
            if character.hp <= 0:

                character.death()
                # Break the game loop
                run = False

            else:
                character.turn()

    # When the game ends this will run
    else:
        print_type(["A GAME BY:\n"])
        time.sleep(.5)
        print("Arctis:   https://github.com/XxArcticAssassinxX")
        print("M0RGANZ:  https://github.com/morganzwest - https://morganz.co.uk")
        print(f"Version: {version}")
        time.sleep(15)  # Hold the window open


if __name__ == "__main__":
    reset()
