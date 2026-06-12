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