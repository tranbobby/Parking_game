from vehicle import Vehicle
class Car(Vehicle):
    def __init__(self, o, r, c, color="grey"):
        super().__init__(o, r, c, 2, color)
