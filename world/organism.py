class Organism(object):

    name = ""
    shortcut = ""
    killed = False
    initiative = 0
    age = 0
    strength = 0
    move_permission = True

    def __init__(self, world, position):
        self.world = world
        self.position = position

    def action(self): pass

    def check_collision(self, other):
        return True

    def collision(self, attacker, defender):
        if isinstance(attacker, defender.__class__) is True:
            print("multiply")
            self.multiply()
            attacker.move_permission = False
            return True
        if self.check_collision(defender) is False:
            print("collision (self) not available")
            return False
        if defender.check_collision(self) is False:
            print("collision (def) not available")
            return False
        if attacker.strength >= defender.strength:
            print("defender killed")
            defender.kill()
            return True
        print("attacker killed")
        attacker.kill()
        return True

    def kill(self):
        self.killed = True

    @property
    def iskilled(self):
        return self.killed

    def multiply(self): pass
