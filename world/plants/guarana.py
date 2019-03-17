from world.plant import Plant


class Guarana(Plant):

    name = "Guarana"
    shortcut = "Gu"

    def check_collision(self, other):
        other.strength(other.strenth() + 3)
        return True