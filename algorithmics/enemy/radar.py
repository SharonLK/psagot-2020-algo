from dataclasses import dataclass

from algorithmics.enemy.threat import Threat
from algorithmics.utils.coordinate import Coordinate


@dataclass
class Radar(Threat):
    center: Coordinate
    radius: float
