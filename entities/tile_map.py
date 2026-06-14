import pygame
from utils import conversion
from .entity import StaticEntity
from pygame import Surface, Vector2
from physics import Transform, RectCollider

class Tile(StaticEntity):
    '''
    지형을 구성하는 타일
    '''
    def __init__(self, size : float, sprite : Surface, position : Vector2):
        transform = Transform(position or Vector2(0, 0))
        super().__init__(
            sprite=sprite,
            transform=transform,
            collider=RectCollider(size, size,  transform)
        )

    def update(self, dt):
        pass

class TileMap:
    def __init__(self, grid, tile_size : float, tile_sprites_dict : dict[int, Surface]):
        '''
        타일을 모아두는 클래스

        Attributes:
            grid (2차원 배열):
                ij 인덱싱 글리드
            grid_size (tuple[float, float]):
                2차원 배열의 모양
            tile_size (float):
                타일 크기(m)
            tile_sprite (Surface):
                타일 이미지
        '''
        self.grid = grid
        self.grid_size = len(grid), len(grid[0])
        self.tile_size = tile_size
        self.tile_sprites_dict = tile_sprites_dict
        
        self.tiles_dict = {}
        self.build_map()
    
    
    def get_tile(self, first : int, second : int, indexing="ij") -> Tile | None:
        '''
        해당 위치의 타일을 반환하는 함수
        indexing == "ij": ij 인덱싱
        indexing == "xy": xy 인덱싱
        '''
        if indexing == "xy": key = (self.grid_size[0] - second - 1, first)
        else: key = (first, second)
        
        return self.tiles_dict.get(key, None)
    
    def get_tiles(self) -> list[Tile]:
        return list(self.tiles_dict.values())

        
    def build_map(self):
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                tile_value = self.grid[i][j]
                if tile_value != 0 and tile_value in self.tile_sprites_dict:
                    tile_position = Vector2(float(j), float(self.grid_size[0] - i - 1)) * self.tile_size
                    sprite = self.tile_sprites_dict[tile_value]
                    self.tiles_dict[(i, j)] = Tile(
                        size=self.tile_size, 
                        sprite=sprite,
                        position=tile_position
                    )

    def render(self, screen : Surface, camera_pos : Vector2):
        width = screen.get_width()
        height = screen.get_height()
        width_meter = conversion.change_px_to_meter(width)
        height_meter = conversion.change_px_to_meter(height)

        start_x = max(int((camera_pos.x - width_meter/2)/self.tile_size)-1, 0)
        start_y = max(int((camera_pos.y - height_meter/2)/self.tile_size)-1, 0)
        
        end_x = min(int((camera_pos.x + width_meter/2)/self.tile_size)+2, self.grid_size[1])
        end_y = min(int((camera_pos.y + height_meter/2)/self.tile_size)+2, self.grid_size[0])
        
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                tile = self.get_tile(x, y, indexing="xy")
                if tile is not None:
                    tile.render(screen, camera_pos)
