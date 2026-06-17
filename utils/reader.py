import os
import pygame
def load_grid_from_file(file_path: str) -> list[list[int]]:
    """
    텍스트 파일을 읽어 2차원 정수형 리스트(Grid)로 변환
    """
    grid = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            # 공백 제거
            tokens = line.strip().split() 
            # 빈 줄 무시
            if not tokens:
                continue 
            
            # 문자열 요소 정수 변환
            row = [int(token) for token in tokens]
            grid.append(row)

    return grid

def load_image_from_file(file_path : str) -> pygame.Surface:
    """
    지정된 경로에서 이미지를 로드 및 투명도 고려
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {file_path}")
        
    try:
        image = pygame.image.load(file_path)
        #image = image.convert()
        #bg_color = image.get_at((0, 0))
        #image.set_colorkey(bg_color)
        
        return image.convert_alpha()
        
    except pygame.error as e:
        raise SystemExit(f"이미지를 로드하는 중 Pygame 에러 발생: {e}")