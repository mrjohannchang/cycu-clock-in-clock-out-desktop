import dataclasses
import enum


class State(enum.IntEnum):
    CLOCK_IN: int = enum.auto()
    CLOCK_OUT: int = enum.auto()


@dataclasses.dataclass
class Url:
    BASE: str = 'https://paperless.cycu.edu.tw/'
    LOGIN: str = '/#/login'
    ATTENDANCE: str = '/#/life/attendance'
