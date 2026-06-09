from collections import defaultdict
from typing import Callable, Any

class EventManager:
    _listeners: dict = defaultdict(list)

    @classmethod
    def subscribe(cls, event_type : str, callback : Callable):
        cls._listeners[event_type].apped(callback)

    @classmethod
    def publish(cls, event_type : str, data : Any = None):
        for callback in cls._listeners.get(event_type, []):
            callback(data)

    @classmethod
    def unsubscribe(cls, event_type: str, callback: Callable):
        cls._listeners[event_type].remove(callback)