from pygame import Vector2, Surface
from .entity import DynamicEntity
from physics.rigidbody2d import RigidBody2D
from physics.transform import Transform
from physics.collider import RectCollider
class Drone(DynamicEntity):
    def __init__(
        self, size : tuple[float, float], sprite : Surface, mass : float = 1.0, moment : float | None = None, 
        position : Vector2 | None = None, velocity : Vector2 | None = None,
        angle : float = 0.0, angular_velocity : float = 0.0,
        collider_scale : tuple[float, float] = (1.0, 1.0)
    ):  
        transform = Transform(position or Vector2(0, 0), angle, size)
        super().__init__(
            sprite=sprite,
            transform=transform,
            collider=RectCollider(size[0] * collider_scale[0], size[1] * collider_scale[1],  transform),
            mass=mass,
            moment=moment,
            velocity=velocity,
            angular_velocity=angular_velocity,
        )

        #region 드론 내부 변수
        self.max_left_thrust = 11.0
        self.max_right_thrust = 11.0
        self.__left_thrust = 0.0
        self.__right_thrust = 0.0

        self.left_arm_position = Vector2(-0.3, 0)
        self.right_arm_position = Vector2(0.3, 0)
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
        return self.__right_thrust
    
    @right_thrust.setter
    def right_thrust(self, val):
        if isinstance(val, float):
            self.__right_thrust = min(self.max_right_thrust, max(0.0, val))

    @property
    def left_velocity(self):
        return self.rigidbody.velocity + RigidBody2D.cross(self.rigidbody.angular_velocity, self.transform.transform_local_vector(self.left_arm_position))
    
    @property
    def right_velocity(self):
        return self.rigidbody.velocity + RigidBody2D.cross(self.rigidbody.angular_velocity, self.transform.transform_local_vector(self.right_arm_position))

    def set_thrust(self, left_thrust : float, right_thrust : float):
        self.left_thrust = left_thrust
        self.right_thrust = right_thrust

    def add_thrust(self, left_thrust : float, right_thrust : float):
        self.left_thrust += left_thrust
        self.right_thrust += right_thrust

    #endregion
    
    def update(self, dt):
        #공기저항
        self.rigidbody.velocity *= 0.95
        self.rigidbody.angular_velocity *= 0.95

        self.rigidbody.apply_force(Vector2(0.0, self.left_thrust), self.left_arm_position, is_local=True)
        self.rigidbody.apply_force(Vector2(0.0, self.right_thrust), self.right_arm_position, is_local=True)

        self.rigidbody.update(dt)
    


        