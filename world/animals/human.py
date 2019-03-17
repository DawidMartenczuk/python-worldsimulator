from world.animal import Animal
from world.position import Position


class Human(Animal):

    name = "Human"
    shortcut = "H"
    strength = 5
    initiative = 4

    special_ability = 5

    def action(self, delta):
        self.special_ability += 1
        if delta == Position(0, 0):
            if self.special_ability >= 5:
                self.special_ability = -5
                self.shortcut = "[H]"
        if self.special_ability == 0:
            self.shortcut = "H"
        if delta.y != 0 and self.world.type == 'hex' and self.position.y % 2 == 1:
            delta.x -= 1
        self.move(Position(delta.x, delta.y) + self.position)

    def check_collision(self, other):
        if self.special_ability < 0:
            other.move_permission = False
            self.move_permission = False
            return False
        return True

