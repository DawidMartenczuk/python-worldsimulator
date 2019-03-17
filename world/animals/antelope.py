import random
from world.animal import Animal


class Antelope(Animal):

    name = "Antelope"
    shortcut = "A"
    initiative = 4
    strength = 4

    def action(self):
        self.move(self.world.nearby_area(self.position, 2))

    def check_collision(self, other):
        if bool(random.getrandbits(1)):
            position = self.world.free_nearby_area(self.position, 1)
            if position == self.position:
                return True
            else:
                self.move(position)
                return True
        return True

