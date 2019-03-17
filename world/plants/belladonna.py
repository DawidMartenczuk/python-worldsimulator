from world.plant import Plant


class Belladonna(Plant):

    name = "Belladonna"
    shortcut = "B"
    strength = 99

    def check_collision(self, other):
        other.kill()
        self.kill()
        return False