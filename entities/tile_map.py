import pygame
from data import TileType
from config import DEFAULT_IMAGE
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
    def __init__(self, grid, tile_size : float, tile_types : dict[int, TileType]):
        self.grid = grid
        self.grid_size = len(grid), len(grid[0])
        self.tile_size = tile_size
        self.tile_types = tile_types
    
    def get_neighbor_mask(self, x, y, tile_value):
        """비트마스킹을 통해 주변 타일의 연결 상태를 계산"""
        mask = 0
        # 상, 하, 좌, 우 (4방향)
        offsets = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for i, (dx, dy) in enumerate(offsets):
            nx, ny = x + dx, y + dy
            if 0 <= ny < self.grid_size[0] and 0 <= nx < self.grid_size[1]:
                if self.grid[ny][nx] == tile_value:
                    mask |= (1 << i)
        return mask

    def render(self, screen : Surface, camera_pos : Vector2):
        from utils import conversion
        width = screen.get_width()
        height = screen.get_height()
        width_meter = conversion.change_px_to_meter(width)
        height_meter = conversion.change_px_to_meter(height)

        start_x = max(int((camera_pos.x - width_meter/2)/self.tile_size)-1, 0)
        start_y = max(int((camera_pos.y - height_meter/2)/self.tile_size)-1, 0)
        
        end_x = min(int((camera_pos.x + width_meter/2)/self.tile_size)+2, self.grid_size[1])
        end_y = min(int((camera_pos.y + height_meter/2)/self.tile_size)+2, self.grid_size[0])
        
        px_size = conversion.change_meter_to_px(Vector2(self.tile_size, self.tile_size))
        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                tile_val = self.grid[y][x]
                if tile_val in self.tile_types:
                    t_type = self.tile_types[tile_val]
                    mask = self.get_neighbor_mask(x, y, tile_val)
                    sprite = t_type.sprite_map.get(mask, t_type.sprite_map.get(0))

                    if sprite is None:
                        sprite = DEFAULT_IMAGE

                    if sprite is not None:
                        scaled_sprite = pygame.transform.scale(sprite, px_size)
                        pos = Vector2(float(x), float(self.grid_size[0] - y - 1)) * self.tile_size
                        screen_pos = conversion.calculate_pos_on_screen(pos, camera_pos, screen)
                        screen.blit(scaled_sprite, scaled_sprite.get_rect(center=screen_pos))

    def get_collidables(self) -> list[Tile]:
        collidable_tiles = []
        for y in range(self.grid_size[0]):
            for x in range(self.grid_size[1]):
                val = self.grid[y][x]
                if val in self.tile_types:
                    t_type = self.tile_types[val]
                    
                    if t_type.is_collidable or t_type.is_solid:
                        pos = Vector2(float(x), float(self.grid_size[0] - y - 1)) * self.tile_size
                        mask = self.get_neighbor_mask(x, y, val)
                        sprite = t_type.sprite_map.get(mask, t_type.sprite_map.get(0))
                        if sprite is None:
                            sprite = DEFAULT_IMAGE
                        px_size = conversion.change_meter_to_px(Vector2(self.tile_size, self.tile_size))
                        scaled_sprite = pygame.transform.scale(sprite, px_size)

                        tile_entity = Tile(self.tile_size, scaled_sprite, pos)
                        tile_entity.is_solid = t_type.is_solid
                        
                        collidable_tiles.append(tile_entity)
        return collidable_tiles