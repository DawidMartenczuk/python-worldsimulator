import random
from world.organism import Organism


class Plant(Organism):

    strength = 0
    initiative = 0

    def multiply(self):
        position = self.world.free_nearby_area(self.position, 1)
        if position == self.position:
            return False
        if random.randrange(0, 10) == 0:
            self.world.add_organism(position, self)

    def action(self):
        self.multiply()