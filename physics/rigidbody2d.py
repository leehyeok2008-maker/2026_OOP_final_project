from pygame import Vector2
from .transform import Transform

class RigidBody2D:
    def __init__(
            self, mass : float, moment : float, transform : Transform,
            velocity : Vector2 | None = None, angular_velocity : float = 0.0
        ):
        '''
        2차원 강체의 역학을 나타내는 클래스.
        
        Attributes:
            mass (float):
                질량

            moment (float):
                관성모멘트
                
            transform (Transform):
                물체 위치 및 자세

            velocity (Vector2):
                질량중심 속도(px/s)

            angular_velocity (float):
                각속도(rad/s)
        '''

        if mass <= 0:
            raise ValueError("Mass must be positive.")
        
        if moment <= 0:
            raise ValueError("Moment must be positive.")

        self.mass = mass
        self.moment = moment

        self.transform = transform
        
        self.velocity = Vector2(0, 0) if velocity is None else Vector2(velocity)
        self.force = Vector2(0, 0)
        
        self.angular_velocity = angular_velocity
        self.torque = 0.0

    @staticmethod
    def cross(vec1 : Vector2, vec2 : Vector2) -> float:
        '''
        2차원 벡터의 외적 연산
        '''
        return vec1.x * vec2.y - vec1.y * vec2.x

    def apply_force(self, force : Vector2, point : Vector2 | None = None, is_local : bool = False):
        '''
        물체에 작용하는 힘과 토크를 추가하는 함수
        is_local == False(default)인 경우, 절대좌표 값으로 고려한다.
        is_local == True인 경우, 해당 물체 기준 상대좌표 값으로 고려한다.
        '''
        if is_local:
            self.force += self.transform.transform_local_vector(force)
            if point is not None: self.torque += self.cross(point, force) 
        else:
            self.force += force
            if point is not None: self.torque += self.cross(point - self.transform.position, force)
    
    def apply_impulse(self, impulse: Vector2, point: Vector2 | None = None, is_local : bool = False):
        '''
        물체에 충격량을 작용하는 함수
        is_local == False(default)인 경우, 절대좌표 값으로 고려한다.
        is_local == True인 경우, 해당 물체 기준 상대좌표 값으로 고려한다.
        '''
        if is_local:
            self.velocity += self.transform.transform_local_vector(impulse / self.mass)
            if point is not None: self.angular_velocity += self.cross(point, impulse) / self.moment
        else:
            self.velocity += impulse / self.mass
            if point is not None: self.angular_velocity += self.cross(point - self.transform.position, impulse) / self.moment
    
    def clear_force(self):
        self.force.update(0, 0)
        self.torque = 0.0

    def update(self, dt : float):
        self.velocity += (self.force / self.mass) * dt
        self.transform.position += self.velocity * dt

        self.angular_velocity += (self.torque / self.moment) * dt
        self.transform.angle += self.angular_velocity * dt

        self.clear_force()
