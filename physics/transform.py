import math
from pygame import Vector2
class Transform:
    def __init__(self, position : Vector2 | None = None, angle : float = 0.0):
        '''
        2차원 물체의 절대 위치 및 자세 정보
        
        Attributes:
            position (Vector2):
                질량중심 위치(px)

            angle (float):
                회전각(rad)
        '''
        
        self.position = Vector2(0, 0) if position is None else position
        self.angle = angle

    #region 내장 유틸리티 함수
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
