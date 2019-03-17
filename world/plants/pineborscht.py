from world.plant import Plant
from world.position import Position


class PineBorscht(Plant):

    name = "Pine Borscht"
    shortcut = "Pb"
    strength = 99

    def action(self):
        if self.world.type == "hex":
            if self.position.y % 2 == 0:
                positions = [
                    Position(self.position.x, self.position.y - 1),
                    Position(self.position.x + 1, self.position.y - 1),
                    Position(self.position.x, self.position.y + 1),
                    Position(self.position.x + 1, self.position.y + 1)
                ]
            else:
                positions = [
                    Position(self.position.x, self.position.y),
                    Position(self.position.x - 1, self.position.y - 1),
                    Position(self.position.x, self.position.y + 1),
                    Position(self.position.x - 1, self.position.y + 1)
                ]
            positions.append(Position(self.position.x - 1, self.position.y))
            positions.append(Position(self.position.x + 1, self.position.y))
        elif self.world.type == "square":
            positions = [
                Position(self.position.x - 1, self.position.y - 1),
                Position(self.position.x - 1, self.position.y),
                Position(self.position.x - 1, self.position.y + 1),
                Position(self.position.x, self.position.y - 1),
                Position(self.position.x, self.position.y + 1),
                Position(self.position.x + 1, self.position.y - 1),
                Position(self.position.x + 1, self.position.y),
                Position(self.position.x + 1, self.position.y + 1),
            ]
        for position in positions:
            organism = self.world.find_organism(position)
            if organism is not None:
                if organism.check_collision(self) is True:
                    organism.kill()
        return True

