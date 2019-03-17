from world.animals.sheep import Sheep
from world.plants.pineborscht import PineBorscht
from world.position import Position


class CyberSheep(Sheep):

    name = "Cyber Sheep"
    shortcut = "CS"
    initiative = 4
    strength = 4

    def check_collision(self, other):
        if isinstance(other, PineBorscht):
            return False

    def action(self):
        so = None
        for x in range(self.world.size.x):
            for y in range(self.world.size.y):
                organism = self.world.find_organism(Position(x, y))
                if organism is not None:
                    if isinstance(organism, PineBorscht):
                        if so is not None:
                            if self.world.distance(self.position, organism.position) < self.world.distance(self.position, so.position):
                                so = organism
                        else:
                            so = organism
        if so is None:
            self.name = "Sheep"
            self.shortcut = "S"
            return Sheep.action(self)
        self.name = "Cyber Sheep"
        self.shortcut = "CS"
        self.move(self.position + Position(self.signum(so.position.x - self.position.x), self.signum(so.position.y - self.position.y)))
        if self.position == so.position:
            so.kill()
        return True

    def signum(self, x):
        if x < 0:
            return -1
        elif x > 0:
            return 1
        else:
            return 0
