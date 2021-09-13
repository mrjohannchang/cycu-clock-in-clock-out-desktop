import dataclasses
import importlib.metadata
import enum


VERSION: str = importlib.metadata.version("cycu-clock-in-clock-out-app")


class State(enum.IntEnum):
    CLOCK_IN: int = enum.auto()
    CLOCK_OUT: int = enum.auto()


@dataclasses.dataclass
class Url:
    BASE: str = 'https://paperless.cycu.edu.tw/'
    LOGIN: str = '/#/login'
    ATTENDANCE: str = '/#/life/attendance'
