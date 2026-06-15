from .controller import Controller
from .pid_controller import PIDController
from entities.drone import Drone
from managers import InputManager
import pygame

class PIDManualController(Controller):
    def __init__(self, drone: Drone):
        super().__init__(drone)
        
        self.pid_y = PIDController(kp=18.0, ki=4.0, kd=8.0)
        self.pid_x = PIDController(kp=10.0, ki=1.0, kd=5.0)
        
        # 최초 시작 위치를 홀드 목표 지점으로 설정
        self.target_x = self.drone.transform.position.x
        self.target_y = self.drone.transform.position.y
        
        self.move_speed = 4.0 

    def command(self, dt: float):
        # 현재 드론의 상태 관측
        current_pos = self.drone.transform.position
        current_vel = self.drone.rigidbody.velocity
        
        # ----------------------------------------------------
        # 1. 좌우(X축) 제어 로직: "누르면 이동, 떼면 그 자리 정지"
        # ----------------------------------------------------
        is_moving_x = False
        target_vel_x = 0.0

        if InputManager.is_key_down(pygame.K_a) or InputManager.is_key_down(pygame.K_LEFT):
            target_vel_x = -self.move_speed
            is_moving_x = True
        elif InputManager.is_key_down(pygame.K_d) or InputManager.is_key_down(pygame.K_RIGHT):
            target_vel_x = self.move_speed
            is_moving_x = True

        if is_moving_x:
            # 💡 키를 누르고 있을 때: 현재 속도가 목표 속도가 되도록 P 제어로 밀어줌
            # (이때는 위치 잠금을 해제하고 실시간으로 타겟 X를 현재 위치로 추적합니다)
            out_x = (target_vel_x - current_vel.x) * 5.0 
            self.target_x = current_pos.x  # 손 떼는 순간 그 자리에 멈추도록 동기화
        else:
            # 💡 키를 뗐을 때: 고정된 target_x를 유지하기 위해 PID 가동 (브레이크 및 위치 고정)
            out_x = self.pid_x.compute(self.target_x, current_pos.x, dt)

        # ----------------------------------------------------
        # 2. 상하(Y축) 제어 로직: "기본적으로 고도 유지"
        # ----------------------------------------------------
        # (원하신다면 여기에 W/S 키로 target_y를 변환하는 코드를 넣으셔도 좋습니다)
        if InputManager.is_key_down(pygame.K_w) or InputManager.is_key_down(pygame.K_UP):
            self.target_y += self.move_speed * dt  # 꾹 누르면 목표 고도 상승

        out_y = self.pid_y.compute(self.target_y, current_pos.y, dt)

        # ----------------------------------------------------
        # 3. PID 출력값을 드론의 좌우 모터 추력(Thrust)으로 믹싱
        # ----------------------------------------------------
        # 드론 물리 공식:
        # - 양쪽 모터를 같이 더하면(out_y) 위로 상승합니다.
        # - 왼쪽 모터를 더하고 오른쪽을 빼면(out_x) 기체가 우측으로 기울며 회전/이동합니다.
        
        # 드론 기본 호버링에 필요한 기초 추력 (중력 상쇄용 베이스라인)
        hover_thrust = (9.81 * self.drone.rigidbody.mass) / 2.0  # 한쪽 모터당 중력의 절반
        
        left_thrust = hover_thrust + out_y + out_x
        right_thrust = hover_thrust + out_y - out_x

        # 최종 연산된 힘을 드론에 주입
        self.drone.set_thrust(left_thrust, right_thrust)