from dataclasses import dataclass

from algorithmics.enemy.threat import Threat
from algorithmics.utils.coordinate import Coordinate


@dataclass
class ObservationPost(Threat):
    """Kidnapper's observation post

    An observation post is defined by its center where the post itself is located, and its detection radius. Note that
    because the view in space is very clear, if the spaceship enters the detection radius of any post, it will be
    detected immediately!

    For more information about observation posts and other threats, refer to this document:
        https://docs.google.com/document/d/16ps7VZRZd3gsKrWACelI3DyU_dNB8ET3lGMScaewams/edit?usp=sharing
    """

    center: Coordinate
    radius: float
