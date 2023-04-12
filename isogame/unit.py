import pygame.transform
from pygame import Rect, Vector2

from isogame.asset_pool import AssetPool
from isogame.unit_command import UnitCommand


UNIT_SIZE = 12, 21
UNIT_WIDTH, UNIT_HEIGHT = UNIT_SIZE


class Unit:
    def __init__(self, position):

        # TODO: animate sprite; make ECS (?)

        # physical component
        self.position = Vector2(position)
        self.move_direction = Vector2()
        self.target_position = None
        self.speed = 32  # px/s

        # executor component
        self.current_command = None
        self.command_queue: list[UnitCommand] = []

        # render component
        self.image = AssetPool.get_image('unit1_idle')
        self.rect = self.image.get_rect(midbottom=position)
        self.facing_right = True

    def update(self, frame_time_s):
        self._execute_commands()

        # moving
        if self.target_position:
            self.move_direction = self.target_position - self.position
            self.move_direction and self.move_direction.normalize_ip()

            self.position += self.move_direction * self.speed * frame_time_s

        # sprite flip
        moving_right = self.move_direction.dot(Vector2(-0.707, 0.707)) < 0
        if (moving_right and not self.facing_right) or \
                (not moving_right and self.facing_right):
            self._flip_image()

    def _flip_image(self):
        self.facing_right = not self.facing_right
        self.image = pygame.transform.flip(self.image, True, False)

    def _execute_commands(self):
        self.current_command.execute() if self.current_command else self.next_command()

    def set_command(self, command: UnitCommand):
        self.command_queue.clear()
        command.set_unit(self)
        self.current_command = command

    def queue_command(self, command: UnitCommand):
        command.set_unit(self)
        self.command_queue.append(command)

    def next_command(self):
        self.current_command = self.command_queue.pop(0) if self.command_queue else None

    def set_destination(self, target_position):
        if Vector2(target_position) != self.target_position:
            self.target_position = Vector2(target_position)

    def has_reached_destination(self):
        return self.position.distance_to(self.target_position) < 3

