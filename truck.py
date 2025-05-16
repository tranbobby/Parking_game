
from vehicle import Vehicle
class Truck(Vehicle):
    def __init__(self, o, r, c, color="blue"):
        super().__init__(o, r, c, 3, color)
