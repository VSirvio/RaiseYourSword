class AiConfig:
    """Stores the configuration for the enemy AI."""

    def __init__(self, idle_time, walk_time, attack_initiation_distance):
        """Creates an AI configuration with the given parameters.

        Args:
            idle_time: A Range of milliseconds the AI stays idle at one time.
            walk_time: A Range of milliseconds the AI keeps walking at one time.
            attack_initiation_distance: Distance in px to player when to attack.
        """

        self.__idle_time = idle_time
        self.__walk_time = walk_time
        self.__attack_initiation_distance = attack_initiation_distance

    @property
    def idle_time(self):
        """Time range for choosing randomly the time for AI to stay idle."""

        return self.__idle_time

    @property
    def walk_time(self):
        """Time range for choosing randomly the time for AI to keep walking."""

        return self.__walk_time

    @property
    def attack_initiation_distance(self):
        """Distance in pixels from the player at which the AI will attack."""

        return self.__attack_initiation_distance
