import math


class Coordinate:
    def __init__(self, x: float, y: float) -> None:
        super().__init__()

        self.x = x
        self.y = y

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Coordinate):
            return False
        return math.fabs(self.x - o.x) <= 1e-6 and math.fabs(self.y - o.y) <= 1e-6

    def __neg__(self) -> 'Coordinate':
        return Coordinate(-self.x, -self.y)

    def __add__(self, other) -> 'Coordinate':
        if not isinstance(other, Coordinate):
            raise TypeError('Addition is allowed only between two coordinates')
        return Coordinate(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> 'Coordinate':
        if not isinstance(other, Coordinate):
            raise TypeError('Subtraction is allowed only between two coordinates')
        return Coordinate(self.x - other.x, self.y - other.y)

    def __truediv__(self, other) -> 'Coordinate':
        if not isinstance(other, (float, int)):
            raise TypeError('Division on coordinate is only possible with a numerical')
        return Coordinate(self.x / other, self.y / other)

    def __mul__(self, other) -> 'Coordinate':
        if not isinstance(other, (float, int)):
            raise TypeError('Multiplication on coordinate is only possible with a numerical')
        return Coordinate(self.x * other, self.y * other)

    def distance_to(self, other: 'Coordinate') -> float:
        """Computes the euclidean distance to the other coordinate
        """
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def __repr__(self) -> str:
        return f'Coordinate(x={self.x}, y={self.y})'

    def __hash__(self) -> int:
        return hash(self.x) ^ hash(self.y)
