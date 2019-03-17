import random
from world.animal import Animal


class Turtle(Animal):

    name = "Turtle"
    shortcut = "T"
    initiative = 1
    strength = 2

    def action(self):
        if random.randrange(1, 100) >= 75:
            return
        self.move(self.world.nearby_area(self.position, 1))

    def check_collision(self, other):
        if other.strength < 5:
            other.move_permission = False
            self.move_permission = False
            return False
        return True

