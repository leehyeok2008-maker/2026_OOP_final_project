import sys
import pygame
from config import *
from scenes import StartScene, GameScene, Scene
from event_manager import EventManager
from input_manager import InputManager

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
        self.current_scene  = StartScene()
        self.scenes : dict[str, Scene]= {
            "START_SCENE" : self.current_scene,
            "GAME_SCENE" : GameScene(),
            #"END_SCENE" : EndScene(),
        }

        self.set_subscription()

    def set_subscription(self):
        EventManager.subscribe("END_GAME", self.end_game)
        EventManager.subscribe("CHANGE_SCENE", self.change_scene)

    #region 기본 반복 코드
    def handle_event(self):
        pg_events = pygame.event.get()
        
        for event in pg_events:
            if event.type == pygame.QUIT:
                self.end_game()

        InputManager.update(pg_events)     

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
    #endregion
    #region 콜백 함수들
    def end_game(self):
        self.is_running = False
    def change_scene(self, val):
        if val in self.scenes.keys():
            self.current_scene = self.scenes[val]
    #endregion