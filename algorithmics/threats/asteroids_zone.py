from dataclasses import dataclass
from typing import List

from algorithmics.threats.threat import Threat
from algorithmics.utils.coordinate import Coordinate


@dataclass
class AsteroidsZone(Threat):
    """Asteroids-attacked zone

    An asteroids-attacked zone (or zone for short) is an area (polygon) in space that has high probability of non-minor
    asteroids circling inside them. Because of the high probability of them being there, and the fact that interaction
    between the spaceship and them is very deadly, the spaceship must never (!!!) enter the boundary of those zones.
    """

    boundary: List[Coordinate]
