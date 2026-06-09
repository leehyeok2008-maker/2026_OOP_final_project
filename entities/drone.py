from pygame import Vector2, Surface
from entity import Entity
from physics.rigidbody2d import RigidBody2D
from physics.transform import Transform
from controller.controller import Controller
from controller.manual_controller import ManualController
class Drone(Entity):
    def __init__(
        self, sprite : Surface, mass : float, moment : float, 
        position : Vector2 | None = None, velocity : Vector2 | None = None,
        angle : float = 0.0, angular_velocity : float = 0.0,
        controller : Controller = ManualController(),
    ):  
        super().__init__(
            sprite=sprite,
            transform=Transform(Vector2(0, 0) if position is None else position, angle)
        )
        self.rigidbody = RigidBody2D(mass, moment, self.transform, Vector2(0, 0) if velocity is None else velocity, angular_velocity)

        self.commands = []
        self.controller = controller

        #region 드론 내부 변수
        self.max_left_thrust = 20.0
        self.max_right_thrust = 20.0

        self.left_arm_position = Vector2(-10.0, 0)
        self.right_arm_position = Vector2(10.0, 0)
        #endregion

    def handle_input(self, inputs):
        self.commands = self.controller.command(inputs)

    def update(self, dt) -> list[str]:
        for command in self.commands:
            if command == "MOVE_UP":
                self.rigidbody.apply_force(Vector2(0, self.max_left_thrust), self.left_arm_position, is_local=True)
                self.rigidbody.apply_force(Vector2(0, self.max_right_thrust), self.right_arm_position, is_local=True)
            if command == "MOVE_DOWN":
                self.rigidbody.apply_force(Vector2(0, 0), self.left_arm_position, is_local=True)
                self.rigidbody.apply_force(Vector2(0, 0), self.right_arm_position, is_local=True)
            if command == "MOVE_LEFT":
                self.rigidbody.apply_force(Vector2(0, -self.max_left_thrust), self.left_arm_position, is_local=True)
                self.rigidbody.apply_force(Vector2(0, self.max_right_thrust), self.right_arm_position, is_local=True)
            if command == "MOVE_RIGHT":
                self.rigidbody.apply_force(Vector2(0, self.max_left_thrust), self.left_arm_position, is_local=True)
                self.rigidbody.apply_force(Vector2(0, -self.max_right_thrust), self.right_arm_position, is_local=True)


        self.rigidbody.update(dt)
        self.commands.clear()
        return []
    


        