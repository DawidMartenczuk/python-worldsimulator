import random
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

class World(object):

    size = None
    organisms = []

    def __init__(self, x, y):
        self.size = Position(x, y)
        self.clear_organisms()

    def clear_organisms(self):
        self.organisms.clear()
        for i in range(10):
            self.organisms.append([])

    def add_organism(self, position, organism):
        if self.isempty(position) is False:
            return None
        class_name = organism.__class__.__name__
        new_organism = eval(class_name)(self, position)
        self.organisms[new_organism.initiative].append(new_organism)
        return new_organism

    def isinworld(self, position):
        if 0 <= position.x < self.size.x and 0 <= position.y < self.size.y:
            return True
        return False

    def isempty(self, position):
        if self.isinworld(position) is False:
            return True
        for i in range(10):
            for organism in self.organisms[i]:
                if organism.position == position:
                    return False
        return True

    def distance(self, position_1, position_2):
        return abs(position_1.x - position_2.x) + abs(position_1.y - position_2.y)

    def nearby_area(self, position, bound):
        while True:
            if self.type == 'hex':
                nearby_position = Position(position.x + random.randint(0, bound), position.y + random.randint(0, bound))
                if (nearby_position.y - position.y) != 0 and position.y % 2 == 1:
                    nearby_position.x -= bound
            elif self.type == 'square':
                nearby_position = Position(position.x + random.randint(bound * -1, bound), position.y + random.randint(bound * -1, bound))
            if self.isinworld(nearby_position) and nearby_position != position:
                return nearby_position

    def free_nearby_area(self, position, bound):
        while True:
            nearby_position = self.nearby_area(position, bound)
            if self.isempty(nearby_position) is True:
                return nearby_position

    def find_organism(self, position):
        for i in range(10):
            for organism in self.organisms[i]:
                if organism.position == position:
                    return organism
        return None

