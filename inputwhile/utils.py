from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
        from collections.abc import Callable

T = TypeVar("T")


def is_parsable(variable: str, class_type: Callable[[str], T]) -> bool:
        try:
                _ = class_type(variable)
                return True
        except ValueError:
                return False
