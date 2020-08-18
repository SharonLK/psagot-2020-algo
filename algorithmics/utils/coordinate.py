import math


class Coordinate:
    def __init__(self, x: float, y: float) -> None:
        """Create a new immutable coordinate

        Note that this class is immutable, any function executed on this class will result in a new Coordinate instance.

        ================================

        >>> c1 = Coordinate(5, 5)
        >>> c2 = Coordinate(10, 10)
        >>> c1
        Coordinate(x=5, y=5)

        >>> c1.x, c1.y
        (5, 5)

        >>> c1.x = 10
        Traceback (most recent call last):
          ...
        AttributeError: can't set attribute

        >>> -c1
        Coordinate(x=-5, y=-5)

        >>> c1 + c2
        Coordinate(x=15, y=15)

        >>> c1.distance_to(c2)
        7.0710678118654755

        :param x: x value of the coordinate
        :param y: y value of the coordinate
        """
        super().__init__()

        self._x = x
        self._y = y

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

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
