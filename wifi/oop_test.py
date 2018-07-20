class Vehicle(object):
    """docstring"""

    def __init__(self, color='', doors='', tires=''):
        """Constructor"""
        self.color = color
        self.doors = doors
        self.tires = tires

    def brake(self):
        """
        Stop the car
        """
        return "Braking"

    def drive(self):
        """
        Drive the car
        """
        return "I'm driving!"

    def __str__(self) -> str:
        return "Vehicle(" \
               "color:'" + self.color +\
               "',doors:'" + self.doors +\
               "',tires:'" + self.tires + "')"


if __name__ == "__main__":
    vehicle = Vehicle()
    vehicle.color = "red"
    vehicle.doors = "hz"
    vehicle.tires = "WTF?"

    print(vehicle)
