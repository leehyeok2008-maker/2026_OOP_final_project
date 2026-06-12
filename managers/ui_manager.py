from pygame import Surface
from ui import UIObject
class UIManager:
    '''
    UI 전반을 관리하는 클래스
    
    Methods:
        add(UIObject):
            ui 오브젝트 추가
        remove(UIObject):
            ui 오브젝트 제거
        render(Surface):
            UI 화면 출력
        update(dt):
            UI 오브젝트 업데이트
    '''
    def __init__(self, ui_objects : list[UIObject] | None = None):
        self.ui_objects : list[UIObject] = ui_objects or []

    def add(self, ui_object : UIObject):
        if ui_object not in self.ui_objects:
            self.ui_objects.append(ui_object)

    def set(self, ui_objects: list[UIObject]):
        self.ui_objects.clear()
        self.ui_objects.extend(ui_objects)

    def remove(self, ui_object: UIObject):
        if ui_object in self.ui_objects:
            self.ui_objects.remove(ui_object)
    
    def update(self, dt):
        for ui_obj in self.ui_objects:
            ui_obj.update(dt)

    def render(self, screen : Surface):
        for ui_obj in self.ui_objects:
            if ui_obj.visible:
                ui_obj.render(screen)


            