from __future__ import annotations

from typing import TYPE_CHECKING, Any, Concatenate, Literal, ParamSpec, TypeVar, overload

import inputwhile.utils as utils

if TYPE_CHECKING:
        from collections.abc import Callable

T = TypeVar("T")
P = ParamSpec("P")
R = TypeVar("R")


@overload
def customFunction(
        prompt: object,
        condition_func: Callable[Concatenate[str, P], R | None],
        error_prompt: object | None,
        doStrip: bool,
        returnValueFromConditionFunc: Literal[False],
        *args: P.args,
        **kwargs: P.kwargs,
) -> str: ...
@overload
def customFunction(
        prompt: object,
        condition_func: Callable[Concatenate[str, P], R | None],
        error_prompt: object | None,
        doStrip: bool,
        returnValueFromConditionFunc: Literal[True],
        *args: P.args,
        **kwargs: P.kwargs,
) -> R: ...
def customFunction(
        prompt: object,
        condition_func: Callable[Concatenate[str, P], R | None],
        error_prompt: object | None = None,
        doStrip: bool = False,
        returnValueFromConditionFunc: bool = False,
        *args: P.args,
        **kwargs: P.kwargs,
) -> str | R:
        """inputwhile for custom conditions.

        Args:
            prompt (object): What will be printed when requesting the input.
            condition_func (Callable[..., Any]): The condition function to be satisfied in order to end the while loop.
            error_prompt (Optional[object], optional): What will be printed when the condition is not satisfied.
                If None uses prompt again. Defaults to None.
            doStrip (bool, optional): Whether to do an element.strip() to the input value. Defaults to False.
            returnValueFromConditionFunc (bool, optional): Whether to return condition_func(value) instead of just value.
                This is usually used in more complex inputwhiles. Defaults to False.

        Returns:
            Any|str: Returns str if returnValueFromConditionFunc is False,
                otherwise returns Any value that condition_func(value) returns
        """
        value = input(prompt).strip() if doStrip else input(prompt)
        condition = condition_func(value, *args, **kwargs)
        while not condition:
                value = input(error_prompt if error_prompt is not None else prompt)
                if doStrip:
                        value = value.strip()
                condition = condition_func(value, *args, **kwargs)
        return condition if returnValueFromConditionFunc else value


ClassType = TypeVar("ClassType", bound=type)


def customTypeClass(
        prompt: object,
        typeClass: Callable[[str], T],
        error_prompt: object | None = None,
        min: Any | None = None,  # noqa: A002, ANN401
        max: Any | None = None,  # noqa: A002, ANN401
) -> T:
        """inputwhile for custom types of variables.

        Args:
            prompt (object): What will be printed when requesting the input.
            typeClass (Type[Any]): The type of the variable to check if value can be parsed to.
            error_prompt (Optional[object], optional): What will be printed when the condition is not satisfied.
                If None uses prompt again. Defaults to None.
            min (Optional[Any], optional): Defines a minimum threshold. Defaults to None.
            max (Optional[Any], optional): Defines a maximum threshold. Defaults to None.

        Returns:
            Any: Returns the input value parsed to the given typeClass.
        """

        def condition_func(value: str) -> bool:
                return (
                        utils.is_parsable(value, typeClass)
                        and (min is None or typeClass(value) >= min)
                        and (max is None or typeClass(value) <= max)
                )

        return typeClass(customFunction(prompt, condition_func, error_prompt))


def integer(
        prompt: object,
        min: int | None = None,  # noqa: A002
        max: int | None = None,  # noqa: A002
        error_prompt: object | None = None,
) -> int:
        """inputwhile for integer values.

        Args:
            prompt (object): What will be printed when requesting the input.
            min (Optional[int], optional): Defines a minimum threshold. Defaults to None.
            max (Optional[int], optional): Defines a maximum threshold. Defaults to None.
            error_prompt (Optional[object], optional): What will be printed when the condition is not satisfied.
                If None uses prompt again. Defaults to None.

        Returns:
            int: Returns an integer value.
        """
        return customTypeClass(prompt, int, error_prompt=error_prompt, min=min, max=max)


def floatInput(
        prompt: object,
        min: float | None = None,  # noqa: A002
        max: float | None = None,  # noqa: A002
        error_prompt: object | None = None,
) -> float:
        """inputwhile for float values.

        Args:
            prompt (object): What will be printed when requesting the input.
            min (Optional[int], optional): Defines a minimum threshold. Defaults to None.
            max (Optional[int], optional): Defines a maximum threshold. Defaults to None.
            error_prompt (Optional[object], optional): What will be printed when the condition is not satisfied.
                If None uses prompt again. Defaults to None.

        Returns:
            float: Returns a float value.
        """
        return customTypeClass(prompt, float, error_prompt=error_prompt, min=min, max=max)


def boolean(
        prompt: object,
        error_prompt: object | None = None,
) -> bool:
        """inputwhile for simple boolean values ("true", "false").

        Args:
            prompt (object): What will be printed when requesting the input.
            error_prompt (Optional[object], optional): What will be printed when the condition is not satisfied.
                If None uses prompt again. Defaults to None.

        Returns:
            bool: Returns a boolean value.
        """
        return booleanFlexible(prompt, error_prompt=error_prompt, trueStrings={"true"}, falseStrings={"false"})


__defaultTrueStrings = {"true", "t", "yes", "y", "1", "si", "sí", "s"}
__defaultFalseStrings = {"false", "f", "no", "n", "0", "nope"}


def booleanFlexible(
        prompt: object,
        error_prompt: object | None = None,
        trueStrings: set[str] = __defaultTrueStrings,
        falseStrings: set[str] = __defaultFalseStrings,
        doUseCustomNDefaults: bool = False,
) -> bool:
        """inputwhile for boolean values that matches more cases:\n
        True for "true", "t", "yes", "y", "1", "si", "sí", "s"

        False for "false", "f", "no", "n", "0", "nope"

        Args:
            prompt (object): What will be printed when requesting the input.
            error_prompt (Optional[object], optional): What will be printed when the condition is not satisfied.
                If None uses prompt again. Defaults to None.
            trueStrings (set[str], optional): Define the string cases when returning true.
                Defaults to {"true", "t", "yes", "y", "1", "si", "sí", "s"}.
            falseStrings (set[str], optional): Define the string cases when returning false.
                Defaults to {"false", "f", "no", "n", "0", "nope"}.
            doUseCustomNDefaults (bool, optional): Whether to mix the strings from the args with the default ones.
                For example, if you want to add more cases without replacing the default ones. Defaults to False.

        Returns:
            bool: Returns a boolean value.
        """
        if doUseCustomNDefaults:
                trueStrings.update(__defaultTrueStrings)
                falseStrings.update(__defaultFalseStrings)

        def condition_func(value: str) -> bool:
                return value.lower() in trueStrings or value.lower() in falseStrings

        return customFunction(prompt, condition_func, error_prompt=error_prompt, doStrip=True).lower() in trueStrings


def booleanFlexibleRegex(
        prompt: object,
        trueRegex: str = r"^(true|yes)$",
        falseRegex: str = r"^(false|no)$",
        error_prompt: object | None = None,
) -> bool:
        """inputwhile for boolean values using regex for True or False.

        Args:
            prompt (object): What will be printed when requesting the input.
            trueRegex (str, optional): The regex to determinate if input value is True. Defaults to r"^(true|yes)$".
            falseRegex (str, optional): The regex to determinate if input value is False. Defaults to r"^(false|no)$".
            error_prompt (Optional[object], optional): What will be printed when the condition is not satisfied.
                If None uses prompt again. Defaults to None.

        Returns:
            bool: Returns a boolean value.
        """
        from re import match

        def condition_func(value: str) -> bool:
                return (
                        match(
                                trueRegex,
                                value.lower(),
                        )
                        is not None
                        or match(
                                falseRegex,
                                value.lower(),
                        )
                        is not None
                )

        return (
                match(
                        trueRegex,
                        customFunction(prompt, condition_func, error_prompt=error_prompt, doStrip=True).lower(),
                )
                is not None
        )


def stringNotEmpty(
        prompt: object,
        error_prompt: object | None = None,
        min: int | None = 1,  # noqa: A002
        max: int | None = None,  # noqa: A002
) -> str:
        """inputwhile for not empty string values.

        Args:
            prompt (object): What will be printed when requesting the input.
            error_prompt (Optional[object], optional): What will be printed when the condition is not satisfied.
                If None uses prompt again. Defaults to None.
            min (Optional[int], optional): Defines a minimum length. Defaults to 1.
            max (Optional[int], optional): Defines a maximum length. Defaults to None.

        Returns:
            str: Returns a string value.
        """

        def condition_func(value: str) -> bool:
                return len(value) >= (min if min is not None and min > 1 else 1) and (max is None or len(value) <= max)

        return customFunction(prompt, condition_func, error_prompt=error_prompt, doStrip=True)


def stringRegex(
        prompt: object,
        regex: str,
        error_prompt: object | None = None,
        min: int | None = None,  # noqa: A002
        max: int | None = None,  # noqa: A002
        doStrip: bool = False,
) -> str:
        """inputwhile for input values that must match a regex.

        Args:
            prompt (object): What will be printed when requesting the input.
            regex (str): The regex pattern to match.
            error_prompt (Optional[object], optional): What will be printed when the condition is not satisfied.
                If None uses prompt again. Defaults to None.
            min (Optional[int], optional): Defines a minimum length. Defaults to None.
            max (Optional[int], optional): Defines a maximum length. Defaults to None.
            doStrip (bool, optional): Whether to do an element.strip() to the input value. Defaults to False.

        Returns:
            str: Returns a string value that matches the regex pattern.
        """
        from re import match

        def condition_func(value: str) -> bool:
                return (
                        match(regex, value) is not None
                        and (min is None or len(value) >= min)
                        and (max is None or len(value) <= max)
                )

        return customFunction(prompt, condition_func, error_prompt=error_prompt, doStrip=doStrip)


def listInput(
        prompt: object,
        separator: str = ",",
        error_prompt: object | None = None,
        map_func: Callable[[str], T] = lambda element: element,
        filter_func: Callable[[str], bool] = lambda _element: True,
        doUseRegex: bool = False,
        doStripElements: bool = False,
) -> list[T]:
        """inputwhile for requesting lists of elements.

        Args:
            prompt (object): What will be printed when requesting the input.
            separator (str, optional): The pattern that separates the elements in the input value. Defaults to ",".
            error_prompt (Optional[object], optional): What will be printed when the condition is not satisfied.
                If None uses prompt again. Defaults to None.
            map_func (_type_, optional): Applies map_func(element) to all the elements. Defaults to lambda element: element.
            filter_func (_type_, optional): Removes elements that filter_func(element) returned False.
                Defaults to lambda _element: True.
            doUseRegex (bool, optional): Whether to use separator as a regex with re.split(separator). Defaults to False.
            doStripElements (bool, optional): Whether to do an element.strip() to all the elements in the list.
                If map_func and filer_func are defined, the element.strip() will be applied *before* the mapping and
                filtering. Defaults to False.

        Returns:
            list[Any|str]: Returns a list of str if map_func is not defined,
                otherwise returns a list of Any value that map_func(element) returns.
        """

        def custom_func(value: str) -> list[T]:
                if doUseRegex:
                        from re import split

                        elements = split(separator, value)
                else:
                        elements = value.split(separator)

                if doStripElements:
                        elements = [element.strip() for element in elements]
                return [map_func(element) for element in elements if filter_func(element)]

        return customFunction(
                prompt,
                custom_func,
                error_prompt=error_prompt,
                doStrip=True,
                returnValueFromConditionFunc=True,
        )


def listRegex(
        prompt: object,
        regex_separator: str = r"[,]+",
        error_prompt: object | None = None,
        map_func: Callable[[str], T] = lambda element: element,
        filter_func: Callable[[str], bool] = lambda _element: True,
        doStripElements: bool = False,
) -> list[T]:
        """inputwhile for requesting lists of elements using regex.

        Args:
            prompt (object): What will be printed when requesting the input.
            regex_separator (str, optional): The regex used to split the input value. Defaults to r"[,]+".
            error_prompt (Optional[object], optional): What will be printed when the condition is not satisfied.
                If None uses prompt again. Defaults to None.
            map_func (_type_, optional): Applies map_func(element) to all the elements. Defaults to lambda element: element.
            filter_func (_type_, optional): Removes elements that filter_func(element) returned False.
                Defaults to lambda _element: True.
            doStripElements (bool, optional): Whether to do an element.strip() to all the elements in the list.
                If map_func and filer_func are defined, the element.strip() will be applied *before* the mapping and
                filtering. Defaults to False.

        Returns:
            list[Any|str]: Returns a list of str if map_func is not defined,
                otherwise returns a list of Any value that map_func(element) returns.
        """
        return listInput(
                prompt,
                error_prompt=error_prompt,
                separator=regex_separator,
                doUseRegex=True,
                map_func=map_func,
                filter_func=filter_func,
                doStripElements=doStripElements,
        )


def setInput(
        prompt: object,
        separator: str = ",",
        error_prompt: object | None = None,
        map_func: Callable[[str], T] = lambda element: element,
        filter_func: Callable[[str], bool] = lambda _element: True,
        doUseRegex: bool = False,
        doStripElements: bool = False,
) -> set[T]:
        """inputwhile for requesting lists of unique elements.

        Args:
            prompt (object): What will be printed when requesting the input.
            separator (str, optional): The pattern that separates the elements in the input value. Defaults to ",".
            error_prompt (Optional[object], optional): What will be printed when the condition is not satisfied.
                If None uses prompt again. Defaults to None.
            map_func (_type_, optional): Applies map_func(element) to all the elements. Defaults to lambda element: element.
            filter_func (_type_, optional): Removes elements that filter_func(element) returned False.
                Defaults to lambda _element: True.
            doUseRegex (bool, optional): Whether to use separator as a regex with re.split(separator). Defaults to False.
            doStripElements (bool, optional): Whether to do an element.strip() to all the elements in the list.
                If map_func and filer_func are defined, the element.strip() will be applied *before* the mapping and
                filtering. Defaults to False.

        Returns:
            set[Any|str]: Returns a set of str if map_func is not defined,
                otherwise returns a set of Any value that map_func(element) returns.
        """
        return set(
                listInput(
                        prompt,
                        error_prompt=error_prompt,
                        separator=separator,
                        doUseRegex=doUseRegex,
                        map_func=map_func,
                        filter_func=filter_func,
                        doStripElements=doStripElements,
                )
        )


def setRegex(
        prompt: object,
        regex_separator: str = r"[,]+",
        error_prompt: object | None = None,
        map_func: Callable[[str], T] = lambda element: element,
        filter_func: Callable[[str], bool] = lambda _element: True,
        doStripElements: bool = False,
) -> set[T]:
        """inputwhile for requesting lists of unique elements using regex.

        Args:
            prompt (object): What will be printed when requesting the input.
            regex_separator (str, optional): The regex used to split the input value. Defaults to r"[,]+".
            error_prompt (Optional[object], optional): What will be printed when the condition is not satisfied.
                If None uses prompt again. Defaults to None.
            map_func (_type_, optional): Applies map_func(element) to all the elements. Defaults to lambda element: element.
            filter_func (_type_, optional): Removes elements that filter_func(element) returned False.
                Defaults to lambda _element: True.
            doStripElements (bool, optional): Whether to do an element.strip() to all the elements in the list.
                If map_func and filer_func are defined, the element.strip() will be applied *before* the mapping and
                filtering. Defaults to False.

        Returns:
            set[Any|str]: Returns a list of str if map_func is not defined,
                otherwise returns a list of Any value that map_func(element) returns.
        """
        return set(
                listInput(
                        prompt,
                        error_prompt=error_prompt,
                        separator=regex_separator,
                        doUseRegex=True,
                        map_func=map_func,
                        filter_func=filter_func,
                        doStripElements=doStripElements,
                )
        )
