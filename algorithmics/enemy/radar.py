from dataclasses import dataclass

from algorithmics.utils.coordinate import Coordinate


@dataclass
class Radar:
    center: Coordinate
    radius: float
