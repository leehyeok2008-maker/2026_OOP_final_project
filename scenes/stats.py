class FlightStats:
    def __init__(
        self, 
        controller: str = "Manual", 
        flight_time: float = 0.0, 
        distance: float = 0.0, 
        collision_time: float = 0.0, 
        energy_used: float = 0.0, 
        score: int = 0
    ):
        
        self.controller = controller
        self.flight_time = flight_time
        self.distance = distance
        self.collision_time = collision_time
        self.energy_used = energy_used
        self.score = score

    def __str__(self) -> str:
        return (f"<FlightStats | Controller: {self.controller}, "
                f"Time: {self.flight_time:.1f}s, Distance: {self.distance:.1f}m, "
                f"Collisions: {self.collision_time}, Energy: {self.energy_used:.1f}%, "
                f"Score: {self.score}>")