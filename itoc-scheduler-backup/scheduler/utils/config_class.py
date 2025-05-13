# Standard Library
from dataclasses import dataclass
from typing import Callable, Union


@dataclass # ?????
class Executor:
    func: Callable
    kwargs: dict


@dataclass
class Job:
    name: str
    enable: bool
    trigger_type: Callable
    trigger_time: list
    execute: Executor
    notify: Union[Executor, None]
