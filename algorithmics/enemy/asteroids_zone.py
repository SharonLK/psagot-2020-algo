from dataclasses import dataclass
from typing import List

from algorithmics.utils.coordinate import Coordinate


@dataclass
class AsteroidsZone:
    boundary: List[Coordinate]
