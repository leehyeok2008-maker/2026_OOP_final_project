from pygame import Surface
from ui.ui_object import UIObject
class UI:
    def __init__(self):
        self.ui_objects : list[UIObject] = []

    def add(self, ui_object : UIObject):
        if ui_object not in self.ui_objects:
            self.ui_objects.append(ui_object)

    def remove(self, ui_object : UIObject):
        self.ui_objects.remove(ui_object)

    def render(self, screen : Surface):
        for ui_obj in self.ui_objects:
            if ui_obj.visible:
                ui_obj.render(screen)

            