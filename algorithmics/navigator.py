from typing import List

from algorithmics.enemy.asteroids_zone import AsteroidsZone
from algorithmics.enemy.observation_post import ObservationPost
from algorithmics.enemy.radar import Radar
from algorithmics.enemy.threat import Threat
from algorithmics.utils.coordinate import Coordinate


def navigate(source: Coordinate, target: Coordinate, threats: List[Threat]) -> List[Coordinate]:
    """Calculates a path from source to target without any detection

    Note: The path must start at the source coordinate and end at the target coordinate!

    :param source: source coordinate of the spaceship
    :param target: target coordinate of the spaceship
    :param threats: list of threats in the scenario (might include any combination of observation posts, asteroids zones
        or radars)
    :return: list of calculated path way points
    """

    observation_posts: List[ObservationPost] = [threat for threat in threats if isinstance(threat, ObservationPost)]
    asteroids_zones: List[AsteroidsZone] = [threat for threat in threats if isinstance(threat, AsteroidsZone)]
    radars: List[Radar] = [threat for threat in threats if isinstance(threat, Radar)]

    # Your objective is to write an algorithm that considering all of the above threats will generate a path that is as
    # short as possible.
    #
    # Note that to be accepted, the returned path must not be detected by the kidnappers at any point, and must not pass
    # through any asteroids zone!

    return [source, target]  # TODO: implement
