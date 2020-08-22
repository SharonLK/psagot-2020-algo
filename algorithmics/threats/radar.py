from dataclasses import dataclass

from algorithmics.threats.threat import Threat
from algorithmics.utils.coordinate import Coordinate


@dataclass
class Radar(Threat):
    """Kidnappers radar

    Radar's are defined by their center where they are located, and a detection radius. When the spaceship is found
    inside the detection radius, it must maintain low enough radial speed to not be detected by the radar.

    For more info and explanation about the allowed radial speed, refer to this document:
        https://docs.google.com/document/d/16ps7VZRZd3gsKrWACelI3DyU_dNB8ET3lGMScaewams/edit?usp=sharing
    """

    center: Coordinate
    radius: float
