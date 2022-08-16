from __future__ import annotations
from typing import Callable

class Event:
    """Event handler
    """
    def __init__(self) -> None:
        self.__events: list[Callable] = []

    def add(self, handler: Callable):
        self.__events.append(handler)
    
    def remove(self, handler: Callable):
        if handler in self.__events:
            self.__events.remove(handler)
        return self

    def __add__(self, other: Callable) -> Event:
        """Use the += operator to add event handler to this event
        """
        self.add(other)
        return self

    def __sub__(self, other: Callable) -> Event:
        """Use the -= operator to remove event handler from this event
        """
        self.remove(other)

    def __call__(self, *args, **kwargs):
        """Call this instance like a function to fire all event handlers
        """
        for handler in self.__events:
            handler(*args, **kwargs)