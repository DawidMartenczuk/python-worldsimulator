from world.organism import Organism


class Animal(Organism):

    def action(self):
        self.move_permission = True
        self.move(self.world.nearby_area(self.position, 1))

    def multiply(self):
        position = self.world.free_nearby_area(self.position, 1)
        if position == self.position:
            return False
        else:
            self.world.add_organism(position, self)

    def move(self, position):
        if self.position == position:
            return False
        if self.world.isinworld(position) is False:
            return False
        if self.world.isempty(position) is True:
            self.position = position
            return True
        enemy = self.world.find_organism(position)
        if enemy.iskilled is False:
            self.collision(self, enemy)
        if self.iskilled is False and self.move_permission is True:
            self.position = position


