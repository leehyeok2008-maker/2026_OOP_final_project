class PIDController:
    def __init__(self, kp: float, ki: float, kd: float):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
        self.integral = 0.0
        self.prev_error = 0.0

    def compute(self, target: float, current: float, dt: float) -> float:
        if dt <= 0.0:
            return 0.0
            
        error = target - current
        
        # P 항 (비례)
        p_term = error * self.kp
        
        # I 항 (적분)
        self.integral += error * dt
        # 누적 폭주 방지 (Windup guard)
        self.integral = max(-5.0, min(5.0, self.integral))
        i_term = self.integral * self.ki
        
        # D 항 (미분)
        derivative = (error - self.prev_error) / dt
        d_term = derivative * self.kd
        
        self.prev_error = error
        return p_term + i_term + d_term

    def reset(self):
        self.integral = 0.0
        self.prev_error = 0.0
        
