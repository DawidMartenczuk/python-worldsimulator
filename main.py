from simulator import Simulator
from world.position import Position

simulator = Simulator(15, 15)
while True:
    inp = input("E: ")
    position = Position(0, 0)
    if inp == 'w':
        position = Position(0, -1)
    elif inp == 's':
        position = Position(0, 1)
    elif inp == 'a':
        position = Position(-1, 0)
    elif inp == 'd':
        position = Position(1, 0)
    elif inp == '[':
        simulator.save()
        continue
    elif inp == ']':
        simulator.load()
        continue
    simulator.execute_turn(position)