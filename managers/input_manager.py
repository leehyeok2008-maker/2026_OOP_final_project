import pygame

class InputManager:
    '''
    사용자 입력 요소를 관리하는 클래스
    '''
    _keys_down = set()
    _keys_pressed = set()
    _keys_released = set()

    _mouse_buttons_down = set()
    _mouse_buttons_pressed = set()
    _mouse_buttons_released = set()

    mouse_pos = (0, 0)

    @classmethod
    def update(cls, events):
        cls._keys_pressed.clear()
        cls._keys_released.clear()

        cls._mouse_buttons_pressed.clear()
        cls._mouse_buttons_released.clear()

        for event in events:

            if event.type == pygame.KEYDOWN:
                if event.key not in cls._keys_down:
                    cls._keys_pressed.add(event.key)

                cls._keys_down.add(event.key)

            elif event.type == pygame.KEYUP:
                cls._keys_down.discard(event.key)
                cls._keys_released.add(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button not in cls._mouse_buttons_down:
                    cls._mouse_buttons_pressed.add(event.button)

                cls._mouse_buttons_down.add(event.button)

            elif event.type == pygame.MOUSEBUTTONUP:
                cls._mouse_buttons_down.discard(event.button)
                cls._mouse_buttons_released.add(event.button)

            elif event.type == pygame.MOUSEMOTION:
                cls.mouse_pos = event.pos

    @classmethod
    def is_key_down(cls, key):
        return key in cls._keys_down

    @classmethod
    def is_key_pressed(cls, key):
        return key in cls._keys_pressed

    @classmethod
    def is_key_released(cls, key):
        return key in cls._keys_released

    @classmethod
    def is_mouse_down(cls, button):
        return button in cls._mouse_buttons_down

    @classmethod
    def is_mouse_pressed(cls, button):
        return button in cls._mouse_buttons_pressed

    @classmethod
    def is_mouse_released(cls, button):
        return button in cls._mouse_buttons_released