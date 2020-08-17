from abc import ABC
from dataclasses import dataclass


@dataclass
class Threat(ABC):
    """Generic kidnappers threat class

    All threat classes inherit from this base class and define objects in space that our spaceship must not be detected
    by.

    For an explanation about the different types of threats and their behavior, refer to this document:
        https://docs.google.com/document/d/16ps7VZRZd3gsKrWACelI3DyU_dNB8ET3lGMScaewams/edit?usp=sharing
    """

    # Feel free to add & implement common methods for threats here
    pass
