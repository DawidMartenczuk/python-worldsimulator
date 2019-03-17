from world.plant import Plant


class SowThistle(Plant):

    name = "SowThistle"
    shortcut = "So"

    def action(self):
        self.multiply()
        self.multiply()
        self.multiply()

