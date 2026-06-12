from collections import defaultdict
from typing import Callable, Any

class EventManager:
    '''
    이벤트를 관리하는 클래스
    
    Methods:
        subscribe(str, Callable): 
            콜백 함수 구독
        publish(str, Any):
            콜백 함수 실행
        unsubscribe(str, Callable):
            콜백 함수 제거
    '''
    _listeners: dict = defaultdict(list)

    @classmethod
    def subscribe(cls, event_type : str, callback : Callable):
        cls._listeners[event_type].append(callback)

    @classmethod
    def publish(cls, event_type : str, data : Any = None):
        print(f"{event_type}: {data} -> {len(cls._listeners.get(event_type, []))}")
        for callback in cls._listeners.get(event_type, []):
            callback(data)

    @classmethod
    def unsubscribe(cls, event_type: str, callback: Callable):
        cls._listeners[event_type].remove(callback)