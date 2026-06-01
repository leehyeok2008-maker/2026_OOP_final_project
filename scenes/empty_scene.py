from pygame import Surface
from pygame.event import Event
from scenes.scene import Scene

class EmptyScene(Scene):
    def handle_event(self, pg_events: list[Event]) -> None:
        return

    def update(self, dt : float) -> list[str]:
        return []
    
    def render(self, screen : Surface) -> None:
        return