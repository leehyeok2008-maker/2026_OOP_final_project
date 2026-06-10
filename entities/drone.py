from pygame import Vector2, Surface
from entity import Entity
from physics.rigidbody2d import RigidBody2D
from physics.transform import Transform
class Drone(Entity):
    def __init__(
        self, sprite : Surface, mass : float, moment : float, 
        position : Vector2 | None = None, velocity : Vector2 | None = None,
        angle : float = 0.0, angular_velocity : float = 0.0,
    ):  
        super().__init__(
            sprite=sprite,
            transform=Transform(position or Vector2(0, 0), angle)
        )
        self.rigidbody = RigidBody2D(mass, moment, self.transform, velocity or Vector2(0, 0), angular_velocity)

        self.commands = []

        #region 드론 내부 변수
        self.max_left_thrust = 20.0
        self.max_right_thrust = 20.0
        self.__left_thrust = 0.0
        self.__right_thrust = 0.0

        self.left_arm_position = Vector2(-10.0, 0)
        self.right_arm_position = Vector2(10.0, 0)
        #endregion

    #region 기타 구현
    @property
    def left_thrust(self):
        return self.__left_thrust
    
    @left_thrust.setter
    def left_thrust(self, val):
        if isinstance(val, float):
            self.__left_thrust = min(self.max_left_thrust, max(0.0, val))

    @property
    def right_thrust(self):
        return self.__left_thrust
    
    @right_thrust.setter
    def right_thrust(self, val):
        if isinstance(val, float):
            self.__right_thrust = min(self.max_right_thrust, max(0.0, val))

    def set_thrust(self, left_thrust : float, right_thrust : float):
        self.left_thrust = left_thrust
        self.right_thrust = right_thrust

    def add_thrust(self, left_thrust : float, right_thrust : float):
        self.left_thrust += left_thrust
        self.right_thrust += right_thrust

    def add_commands(self, commands : list[str]):
        self.commands += commands
    #endregion
    
    def update(self, dt):
        self.set_thrust(0.0, 0.0)
        for command in self.commands:
            if command == "MOVE_UP": self.add_thrust(self.max_left_thrust, self.max_right_thrust)
            if command == "MOVE_DOWN": self.add_thrust(0.0, 0.0)
            if command == "MOVE_LEFT": self.add_thrust(0.0, self.max_right_thrust)
            if command == "MOVE_RIGHT": self.add_thrust(self.max_left_thrust, 0.0)

        self.rigidbody.apply_force(Vector2(0.0, self.left_thrust), self.left_arm_position, is_local=True)
        self.rigidbody.apply_force(Vector2(0.0, self.right_thrust), self.right_arm_position, is_local=True)
        self.rigidbody.update(dt)
        self.commands.clear()
    


        