import os
import json

from world.world import World
from world.position import Position
from world.animals.antelope import Antelope
from world.animals.fox import Fox
from world.animals.human import Human
from world.animals.sheep import Sheep
from world.animals.cybersheep import CyberSheep
from world.animals.turtle import Turtle
from world.animals.wolf import Wolf
from world.plants.belladonna import Belladonna
from world.plants.grass import Grass
from world.plants.guarana import Guarana
from world.plants.sowthistle import SowThistle
from world.plants.pineborscht import PineBorscht


class Simulator(World):

    file = 'level.txt'

    def __init__(self, x, y, type):
        World.__init__(self, x, y)
        self.window = None
        self.turn = 0
        self.type = type
        self.generate_world()
        self.init_window(x, y)

    def init_window(self, x, y):
        if self.window is not None:
            """close window"""
        """open window"""
        self.render()

    def generate_world(self): pass

    def save(self):
        with open(self.file, "w+") as ins:
            ins.write(str(self.size.x) + " " + str(self.size.y) + " " + self.type + " \n")
            for i in range(10):
                for organism in self.organisms[i]:
                    text = organism.__class__.__name__ + " " + str(organism.position.x) + " " + str(organism.position.y) + " " + str(organism.age) + " " + str(organism.strength)
                    if isinstance(organism, Human):
                        text += " " + str(organism.special_ability)
                    ins.write(text + " \n")
            ins.close()

    def load(self):
        with open(self.file, "r") as ins:
            initiative = 0
            read_world_data = True
            for line in ins:
                exp = line.split(' ')
                if read_world_data is not True:
                    print(exp)
                    position = Position(int(exp[1]), int(exp[2]))
                    organism = self.add_organism(position, eval(exp[0])(self, position))
                    self.find_organism(position)
                    organism.age = int(exp[3])
                    organism.strength = int(exp[4])
                    if isinstance(organism, Human):
                        organism.special_ability = int(exp[5])
                        if organism.special_ability < 0:
                            organism.shortcut = '[H]'
                        print(str(organism.special_ability))
                else:
                    read_world_data = False
                    self.size = Position(int(exp[0]), int(exp[1]))
                    self.type = exp[2]
                    self.clear_organisms()
            self.init_window(self.size.x, self.size.y)
            ins.close()

    def execute_turn(self, move):
        self.turn += 1
        ability = 0
        for i in range(10):
            for organism in self.organisms[i]:
                if organism.iskilled:
                    continue
                organism.age = organism.age + 1
                if isinstance(organism, Human):
                    organism.action(move)
                    continue
                organism.action()
        self.kill_all()
        self.render()

    def render(self):
        clear = lambda: os.system('cls')
        clear()
        print("\tturn: " + str(self.turn))
        for i in range(10):
            for organism in self.organisms[i]:
                print(str(organism) + "(" + str(organism.age) + "): " + str(organism.position.x) + ", " + str(organism.position.y) + "; " + str(organism.iskilled))
        for y in range(self.size.y):
            text = ""
            for x in range(self.size.x):
                organism = self.find_organism(Position(x, y))
                if organism is not None:
                    text += organism.shortcut.rjust(3, ' ')
                else:
                    text += "   "
            print(text)
        return True

    def kill_all(self):
        for i in range(10):
            for organism in self.organisms[i]:
                if organism.iskilled:
                    self.organisms[i].remove(organism)

