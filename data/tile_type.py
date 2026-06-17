from pygame import Surface
class TileType:
    def __init__(self, name: str, sprite_map: dict[int, Surface], is_solid: bool = True, is_collidable: bool = True):
        self.name = name
        self.sprite_map = sprite_map
        self.is_solid = is_solid          # 밀려나는 물리 법칙 적용 여부
        self.is_collidable = is_collidable  # ColliderManager에 등록할지 여부
