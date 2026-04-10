from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def is_parsable(variable: str, class_type: Callable[[str], T]) -> bool:
        try:
                _ = class_type(variable)
                return True
        except ValueError:
                return False
