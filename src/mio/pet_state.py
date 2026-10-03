"""Mio pet state model.

Defines the semantic states representing what the pet is currently doing.
This is an application-coordination concern, independent from animation
assets or presentation details.

The state model should remain minimal. Only states justified by
actually implemented functionality should be added.
"""

from enum import Enum, auto


class PetState(Enum):
    """Semantic state of the Mio pet.

    Each value represents a distinct behavioral/presentation context.
    Animation (Step 5) will later use these states to select visuals,
    but the state model itself has no knowledge of animation assets.

    Values:
        IDLE: The pet is sitting on the desktop with no active interaction.
        DRAGGING: The pet is being repositioned by the user via mouse drag.
    """

    IDLE = auto()
    DRAGGING = auto()
