from abc import ABC


class UnitCommand(ABC):
    def __init__(self):
        self.unit = None

    def set_unit(self, unit):
        self.unit = unit

    def execute(self):
        pass

    def finish(self):
        self.unit.next_command()
        self.unit = None

    def is_finished(self):
        return self.unit is None


# do I need it?
class UnitCommandIdle(UnitCommand):
    pass


class UnitCommandMove(UnitCommand):
    def __init__(self, target_position):
        super().__init__()
        self.target_position = target_position

    def execute(self):
        self.unit.set_destination(self.target_position)

        if self.unit.has_reached_destination():
            self.finish()

    def finish(self):
        self.unit.target_position = None
        super().finish()


class UnitCommandFollow(UnitCommand):
    def __init__(self, target_unit):
        super().__init__()
        self.target_unit = target_unit


class UnitCommandAttack(UnitCommand):
    def __init__(self, target_unit):
        super().__init__()
        self.target_unit = target_unit
