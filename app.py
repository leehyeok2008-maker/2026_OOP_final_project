import sys
import pygame
from config import *
from input import Input
from scenes.scene import Scene
from scenes.empty_scene import EmptyScene
from event_manager import EventManager

class App():
    def __init__(self):
        pygame.init()

        self.screen_width = WIDTH
        self.screen_height = HEIGHT
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        pygame.display.set_caption(APP_NAME)

        self.background_color = BACKGROUND_COLOR
        self.clock = pygame.time.Clock()
        self.fps = FPS
        self.dt = 0.0

        self.is_running = True
        self.current_scene  = EmptyScene() # 나중에 진짜 기본 Scene (StartScene)으로 수정
        self.scenes = {}
    
    def handle_event(self):
        pg_events = pygame.event.get()
        
        for event in pg_events:
            if event.type == pygame.QUIT:
                self.is_running = False

        Input.update(pg_events)        

    def update(self):
        self.current_scene.update(self.dt)
    
    def render(self):
        self.screen.fill(self.background_color)
        self.current_scene.render(self.screen)
        pygame.display.flip()

    def run(self):
        while self.is_running:
            self.dt = self.clock.tick(self.fps) / 1000
            self.handle_event()
            self.update()
            self.render()

        pygame.quit()
        sys.exit()