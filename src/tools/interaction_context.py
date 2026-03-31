from __future__ import annotations

from typing import Callable, Optional


ConfirmationHandler = Callable[[str, str, str, str], bool]
NumberHandler = Callable[[str, str, int, int], int]


_confirmation_handler: Optional[ConfirmationHandler] = None
_number_handler: Optional[NumberHandler] = None


def set_confirmation_handler(handler: Optional[ConfirmationHandler]) -> None:
    global _confirmation_handler
    _confirmation_handler = handler


def set_number_handler(handler: Optional[NumberHandler]) -> None:
    global _number_handler
    _number_handler = handler


def request_confirmation(
    title: str,
    message: str,
    confirm_label: str = "Yes",
    cancel_label: str = "No",
) -> bool:
    if _confirmation_handler is not None:
        return _confirmation_handler(title, message, confirm_label, cancel_label)

    prompt = f"\n{title}\n{message}\n({confirm_label}/{cancel_label}): "
    return input(prompt).strip().lower().startswith(confirm_label[:1].lower())


def request_number(
    title: str,
    message: str,
    default: int = 0,
    minimum: int = 0,
) -> int:
    if _number_handler is not None:
        return _number_handler(title, message, default, minimum)

    prompt = f"\n{title}\n{message}\n[{default}]: "
    user_input = input(prompt).strip()
    if not user_input:
        return default

    value = int(user_input)
    return max(value, minimum)
