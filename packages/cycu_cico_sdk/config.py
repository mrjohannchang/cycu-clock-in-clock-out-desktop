import dataclasses
import datetime
import logging
import pathlib
from typing import Any, IO, Optional

import dacite
import toml

CONFIG_VERSION: int = 1
CONFIG_FILENAME: str = 'config.toml'
CONFIG_PATH: pathlib.Path = pathlib.Path.cwd() / CONFIG_FILENAME


@dataclasses.dataclass
class Config:
    data_version: int = CONFIG_VERSION
    active_tab: int = 0
    account: str = ''
    password: str = ''
    clock_in_start_time: datetime.time = datetime.time(7, 30)
    clock_in_end_time: datetime.time = datetime.time(8, 30)
    clock_out_start_time: datetime.time = datetime.time(17, 0)
    clock_out_end_time: datetime.time = datetime.time(17, 30)
    exclude_weekends: bool = True
    exclude_specific_dates: bool = True
    specific_dates: list[str] = dataclasses.field(default_factory=lambda: ['2021-09-20', '2021-09-21'])


def get_config() -> Config:
    global config

    if not config:
        try:
            config_dict: dict[str, Any] = toml.load(CONFIG_PATH)
            config = dacite.from_dict(data_class=Config, data=config_dict)
        except FileNotFoundError:
            pass
        except Exception as e:
            logging.exception(e)

    if not config:
        config = Config()
        save_config()
    return config


def save_config():
    try:
        f: IO
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            toml.dump(dataclasses.asdict(config), f)
    except Exception as e:
        logging.exception(e)


config: Optional[Config] = None
