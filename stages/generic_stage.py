from .stage import Stage
from typing import Callable
from entities import Drone, Cargo, TileMap, Goal
from controllers import Controller, ManualController
from utils import reader
from config import DEFAULT_TILE_TYPE
import pygame
from pygame import Vector2

class GenericStage(Stage):
    def __init__(
        self, 
        map_path: str, 
        drone_pos: Vector2, 
        cargo_pos: Vector2, 
        goal_pos: Vector2, 
        goal_condition : str = "CARGO_ONLY", 
        has_cargo : bool = True, 
        goal_event : Callable[[], None] = lambda: None,
        controller : type[Controller] = ManualController
    ):
        tile_map = TileMap(
            grid=reader.load_grid_from_file(map_path),
            tile_size=1.0,
            tile_types=DEFAULT_TILE_TYPE
        )
        
        drone = Drone((2.0, 2.0), [reader.load_image_from_file(f"images/drone/drone_animation_{i}.png") for i in range(1, 9)], 1, position=drone_pos, collider_scale=(0.8, 0.55))
        cargo = None if not has_cargo else Cargo((1.2, 1.2), reader.load_image_from_file("images/cargo.png"), 1, position=cargo_pos)
        goal = Goal((1.5, 1.5), reader.load_image_from_file("images/goal.png"), 1, position=goal_pos, condition_type=goal_condition, goal_event=goal_event)
        
        super().__init__(
            drone=drone,
            cargo=cargo,
            tile_map=tile_map,
            controller=controller(drone),
            goal=goal,
        )