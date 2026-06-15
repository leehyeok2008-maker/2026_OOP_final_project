import math
import matplotlib.pyplot as plt
from .controller import Controller
from .pid_controller import PIDController
from entities.drone import Drone, Cargo
from managers import InputManager
import pygame

class PIDManualController(Controller):
    def __init__(self, drone: Drone):
        super().__init__(drone)
        
        self.pid_vx = PIDController(kp=150.0, ki=10.0, kd=10.0)
        self.pid_vy = PIDController(kp=300.0, ki=10.0, kd=10.0)
        self.pid_ang = PIDController(kp=100.0, ki=10.0, kd=5.0)
        
        self.speed_x = 3.5
        self.speed_y = 3.5

        # --- Matplotlib 데이터 기록용 변수 ---
        self.time_elapsed = 0.0
        self.history_t = []
        self.history_vx = []
        self.history_target_vx = []
        self.history_vy = []
        self.history_target_vy = []
        self.history_ang = []

    def command(self, dt: float, **kwargs):
        grav_acc = kwargs.get("grav_acc", 9.8)
        current_vel = self.drone.rigidbody.velocity
        current_ang = self.drone.transform.angle

        max_left_thrust = self.drone.max_left_thrust
        max_right_thrust = self.drone.max_right_thrust
        max_angle = 0.6

        target_vx = 0.0
        target_vy = 0.0

        # 입력 처리 (목표 속도 설정)
        if InputManager.is_key_down(pygame.K_a) or InputManager.is_key_down(pygame.K_LEFT):
            target_vx = -self.speed_x
        elif InputManager.is_key_down(pygame.K_d) or InputManager.is_key_down(pygame.K_RIGHT):
            target_vx = self.speed_x
            
        if InputManager.is_key_down(pygame.K_w) or InputManager.is_key_down(pygame.K_UP):
            target_vy = self.speed_y
        elif InputManager.is_key_down(pygame.K_s) or InputManager.is_key_down(pygame.K_DOWN):
            target_vy = -self.speed_y

        # PID 제어 연산 (Cascade 구조)
        out_vy = self.pid_vy.compute(target_vy, current_vel.y, dt)
        base_thrust = self.drone.rigidbody.mass * grav_acc
        cos_ang = max(math.cos(current_ang), 0.1)
        total_thrust = (base_thrust + out_vy) / cos_ang

        out_vx = self.pid_vx.compute(target_vx, current_vel.x, dt)
        target_angle = -out_vx 
        target_angle = max(-max_angle, min(max_angle, target_angle))

        out_ang = self.pid_ang.compute(target_angle, current_ang, dt)

        # 모터 출력 분배
        left_thrust = (total_thrust / 2.0) - out_ang
        right_thrust = (total_thrust / 2.0) + out_ang

        left_thrust = max(0.0, min(max_left_thrust, left_thrust))
        right_thrust = max(0.0, min(max_right_thrust, right_thrust))

        self.drone.set_thrust(left_thrust, right_thrust)

        # --- 데이터 로깅 업데이트 ---
        self.time_elapsed += dt
        self.history_t.append(self.time_elapsed)
        self.history_vx.append(current_vel.x)
        self.history_target_vx.append(target_vx)
        self.history_vy.append(current_vel.y)
        self.history_target_vy.append(target_vy)
        self.history_ang.append(math.degrees(current_ang))

        # [그래프 출력 트리거] P 키를 누르면 그래프 창 생성
        if InputManager.is_key_pressed(pygame.K_p):
            self.show_plot()

        #region 로프 액션
        if InputManager.is_key_pressed(pygame.K_r):
            if self.drone.is_holding:
                self.drone.is_holding = False
            else:
                for other in self.drone.collision_list:
                    rope_length = float('inf')
                    attached_cargo = None
                    if isinstance(other, Cargo):
                        distance = self.drone.anchor_point.distance_to(other.transform.position)
                        if distance <= rope_length:
                            self.drone.is_holding = True
                            rope_length = distance
                            attached_cargo = other
                    self.drone.rope_length = rope_length
                    self.drone.attached_cargo = attached_cargo
                        
        if InputManager.is_key_down(pygame.K_e):
            self.drone.rope_length += self.drone.rope_speed * dt
        
        if InputManager.is_key_down(pygame.K_q):
            self.drone.rope_length -= self.drone.rope_speed * dt
        #endregion

    def show_plot(self):
        """저장된 비행 데이터를 바탕으로 Matplotlib 그래프를 출력합니다."""
        plt.figure(figsize=(10, 8))
        plt.suptitle("Pygame Drone Velocity & Attitude Control", fontsize=16)

        # 1. X축 속도 추종 그래프
        plt.subplot(3, 1, 1)
        plt.plot(self.history_t, self.history_target_vx, label="Target VX (Input)", linestyle='--', color='red')
        plt.plot(self.history_t, self.history_vx, label="Current VX", color='blue')
        plt.title("X Velocity Control (Left/Right)")
        plt.ylabel("Velocity")
        plt.grid(True)
        plt.legend()

        # 2. Y축 속도 추종 그래프
        plt.subplot(3, 1, 2)
        plt.plot(self.history_t, self.history_target_vy, label="Target VY (Input)", linestyle='--', color='red')
        plt.plot(self.history_t, self.history_vy, label="Current VY", color='green')
        plt.title("Y Velocity Control (Up/Down)")
        plt.ylabel("Velocity")
        plt.grid(True)
        plt.legend()

        # 3. 드론 자세(기울기) 그래프
        plt.subplot(3, 1, 3)
        plt.plot(self.history_t, self.history_ang, label="Pitch Angle (deg)", color='orange')
        plt.axhline(0, color='gray', linestyle='--')
        plt.title("Drone Pitch Angle")
        plt.xlabel("Time (s)")
        plt.ylabel("Angle (degrees)")
        plt.grid(True)
        plt.legend()

        plt.tight_layout()
        plt.show()