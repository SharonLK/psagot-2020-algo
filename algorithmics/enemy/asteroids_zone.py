from dataclasses import dataclass
from typing import List

from algorithmics.enemy.threat import Threat
from algorithmics.utils.coordinate import Coordinate


@dataclass
class AsteroidsZone(Threat):
    boundary: List[Coordinate]
