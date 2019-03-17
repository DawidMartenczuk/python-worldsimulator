from world.animal import Animal


class Fox(Animal):

    name = "Fox"
    shortcut = "F"
    initiative = 7
    strength = 3

    def action(self):
        attempts = 10
        position = None
        while True:
            if attempts == 0:
                return False
            position = self.world.nearby_area(self.position, 1)
            attempts -= 1
            if self.world.isempty(position) is True or self.world.find_organism(position).strength < self.strength:
                break
        self.move(position)
        return True