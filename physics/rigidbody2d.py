import math
from pygame import Vector2
class RigidBody2D:
    def __init__(
            self, mass : float, moment : float, 
            position : Vector2 | None = None, velocity : Vector2 | None = None, 
            angle : float = 0.0, angular_velocity : float = 0.0
        ):
        '''
        2차원 강체의 역학을 나타내는 클래스.
        
        Attributes:
            mass (float):
                질량

            moment (float):
                관성모멘트

            position (Vector2):
                질량중심 위치(px)

            velocity (Vector2):
                질량중심 속도(px/s)

            angle (float):
                회전각(rad)

            angular_velocity (float):
                각속도(rad/s)
        '''

        if mass <= 0:
            raise ValueError("Mass must be positive.")
        
        if moment <= 0:
            raise ValueError("Moment must be positive.")

        self.mass = mass
        self.moment = moment
        
        self.position = Vector2(0, 0) if position is None else Vector2(position)
        self.velocity = Vector2(0, 0) if velocity is None else Vector2(velocity)
        self.force = Vector2(0, 0)
        
        self.angle = angle
        self.angular_velocity = angular_velocity
        self.torque = 0.0

    #region 내장 유틸리티 함수
    @staticmethod
    def cross(vec1 : Vector2, vec2 : Vector2) -> float:
        '''
        2차원 벡터의 외적 연산
        '''
        return vec1.x * vec2.y - vec1.y * vec2.x
    
    def transform_local_vector(self, vec : Vector2) -> Vector2:
        '''
        상대좌표 벡터를 절대좌표 벡터로 변환.
        (물체 방향에 따라 회전.)
        '''
        return vec.rotate(math.degrees(self.angle))
    
    def transform_absolute_vector(self, vec : Vector2) -> Vector2:
        '''
        절대좌표 벡터를 상대좌표 벡터로 변환.
        (물체 방향에 따라 회전)
        '''
        return vec.rotate(math.degrees(-self.angle))
    
    def transform_local_position(self, vec : Vector2) -> Vector2:
        '''
        상대좌표 위치를 절대좌표 위치로 변환.
        (물체 방향에 따라 회전 및 평행이동)
        '''
        return vec.rotate(math.degrees(self.angle)) + self.position
    
    def transform_absolute_position(self, vec : Vector2) -> Vector2:
        '''
        절대좌표 위치를 상대좌표 위치로 변환.
        (물체 방향에 따라 회전 및 평행이동)
        '''
        return vec.rotate(math.degrees(-self.angle)) - self.position
    #endregion

    def apply_force(self, force : Vector2, point : Vector2 | None = None, is_local : bool = False):
        '''
        물체에 작용하는 힘과 토크를 추가하는 함수
        is_local == False(default)인 경우, 절대좌표 값으로 고려한다.
        is_local == True인 경우, 해당 물체 기준 상대좌표 값으로 고려한다.
        '''
        if is_local:
            self.force += self.transform_local_vector(force)
            if point is not None: self.torque += self.cross(point, force) 
        else:
            self.force += force
            if point is not None: self.torque += self.cross(point - self.position, force)

    def clear_force(self):
        self.force.update(0, 0)
        self.torque = 0.0

    def update(self, dt : float):
        self.velocity += (self.force / self.mass) * dt
        self.position += self.velocity * dt

        self.angular_velocity += (self.torque / self.moment) * dt
        self.angle += self.angular_velocity * dt

        self.clear_force()
