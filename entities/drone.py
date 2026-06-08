from pygame import Vector2, Surface
from entity import Entity
from physics.rigidbody2d import RigidBody2D
from controller.controller import Controller
from controller.manual_controller import ManualController
class Drone(Entity):
    def __init__(
        self, sprite : Surface, mass : float, moment : float, 
        position : Vector2 | None = None, velocity : Vector2 | None = None,
        angle : float = 0.0, angular_velocity : float = 0.0,
        controller : Controller = ManualController(),
    ):  
        self.commands = []
        self.controller = controller
        super().__init__(
            sprite=sprite,
            rigidbody=RigidBody2D(mass, moment, position, velocity, angle, angular_velocity)
        )

    def handle_input(self, inputs):
        self.commands = self.controller.command(inputs)

    def update(self, dt) -> list[str]:
        self.rigidbody.update(dt)
        self.commands.clear()
        return []
    


        