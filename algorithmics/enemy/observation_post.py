from dataclasses import dataclass

from algorithmics.utils.coordinate import Coordinate


@dataclass
class ObservationPost:
    center: Coordinate
    radius: float
