from __future__ import annotations
from typing import Callable

class EventHandler:
    """This should be subclassed
    and used from the super class
    """
    def __init__(self) -> None:
        self.__events: dict[str, list[Callable]] = {}

    def on(self, event: str, handler: Callable):
        """Add an event handler

        Args:
            event (str): Event name
            handler (Callable): Event handler
        """
        if event not in self.__events:
            self.__events[event] = []

        self.__events[event].append(handler)

    def remove(self, event: str, handler: Callable = None) -> None:
        """Remove an event handler

        Args:
            event (str): Event name
            handler (Callable, optional): Event handler. Defaults to None (remove all event handlers for event name).
        """
        if handler == None:
            if event in self.__events:
                del self.__events[event]
                return

        for name, handlers in self.__events.items():
            if name == event:
                if handler in handlers:
                    handlers.remove(handler)
                return

    def fire(self, event: str, *args, **kwargs) -> None:
        """Fire an event handler

        Args:
            event (str): Event name
        """
        for name, handlers in self.__events.items():
            if name == event:
                for handler in handlers:
                    handler(*args, **kwargs)
                return