import math
from pygame import Vector2, Surface
from .entity import DynamicEntity
from .cargo import Cargo
from .tile_map import Tile
from physics.rigidbody2d import RigidBody2D
from physics.transform import Transform
from physics.collider import RectCollider
from managers.event_manager import EventManager

class Drone(DynamicEntity):
    def __init__(
        self, size : tuple[float, float], sprite_sheets : list[Surface], mass : float = 1.0, moment : float | None = None, 
        position : Vector2 | None = None, velocity : Vector2 | None = None,
        angle : float = 0.0, angular_velocity : float = 0.0,
        collider_scale : tuple[float, float] = (1.0, 1.0)
    ):  
        
        self.sprite_frames = sprite_sheets if sprite_sheets else [Surface(size)]
        self.current_frame_idx = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.05

        transform = Transform(position, angle, size)
        super().__init__(
            sprite=self.sprite_frames[self.current_frame_idx],
            transform=transform,
            collider=RectCollider(size[0] * collider_scale[0], size[1] * collider_scale[1],  transform),
            mass=mass,
            moment=moment,
            velocity=velocity,
            angular_velocity=angular_velocity,
        )

        #region 드론 내부 변수
        self.is_holding = False
        self.attached_cargo : None | Cargo= None
        self.rope_anchor_offset = Vector2(0.0, -size[1] * collider_scale[1] / 2)
        self.rope_speed = 1.0
        self.min_rope_length = size[1] * collider_scale[1]
        self.max_rope_length = 6.0
        self.__rope_length = self.min_rope_length

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

    @property
    def rope_length(self):
        return self.__rope_length
    
    @property
    def anchor_point(self):
        return self.transform.transform_local_position(self.rope_anchor_offset)
    
    @rope_length.setter
    def rope_length(self, val):
        if isinstance(val, float):
            self.__rope_length = min(self.max_rope_length, max(self.min_rope_length, val))

    def set_thrust(self, left_thrust : float, right_thrust : float):
        self.left_thrust = left_thrust
        self.right_thrust = right_thrust

    def add_thrust(self, left_thrust : float, right_thrust : float):
        self.left_thrust += left_thrust
        self.right_thrust += right_thrust

    #endregion
    
    def _update_animation(self, dt):
        if self.left_thrust > 0.1 or self.right_thrust > 0.1:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0.0
                self.current_frame_idx = (self.current_frame_idx + 1) % len(self.sprite_frames)
                
                self.sprite = self.sprite_frames[self.current_frame_idx]
        else:
            self.current_frame_idx = 0
            self.sprite = self.sprite_frames[0]

    def update(self, dt):
        if abs(self.transform.angle) > (math.pi / 2) * 0.75:
            EventManager.publish("FAIL_STAGE", "제어 실패")
        EventManager.publish("SET_HOLDING_TEXT", self.is_holding)
        
        #공기저항
        self.rigidbody.velocity *= 0.97
        self.rigidbody.angular_velocity *= 0.97

        self.rigidbody.apply_force(Vector2(0.0, self.left_thrust), self.left_arm_position, is_local=True)
        self.rigidbody.apply_force(Vector2(0.0, self.right_thrust), self.right_arm_position, is_local=True)
        self._update_animation(dt)

        super().update(dt)
            
            
            
    


        