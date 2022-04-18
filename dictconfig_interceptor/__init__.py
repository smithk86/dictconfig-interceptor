from __future__ import annotations

import logging.config
from contextvars import ContextVar
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from typing import Any, Callable, Dict, List, Optional, Iterator
    from logging.config import _DictConfigArgs


_callback_var: ContextVar[Optional[dictConfigCallbacks]] = ContextVar(
    "callbacks", default=None
)


class dictConfigCallbacks:
    def __init__(self):
        self.funcs: List[Callable] = list()

    def __call__(self, func: Callable) -> None:
        self.funcs.append(func)

    def __iter__(self) -> Iterator[Callable]:
        return iter(self.funcs)

    def __enter__(self) -> dictConfigCallbacks:
        _callback_var.set(self)
        return self

    def __exit__(self, *exc) -> None:
        pass


def dictConfig(config: _DictConfigArgs | Dict[str, Any]) -> None:
    _callbacks = _callback_var.get()
    if _callbacks:
        for func in _callbacks:
            func(config)
    config_class = logging.config.dictConfigClass(config)  # type: ignore
    config_class.configure()


setattr(logging.config, "dictConfig", dictConfig)
