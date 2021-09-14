import asyncio
import dataclasses
import datetime
import logging
import os
import random
import re
import shutil
import stat
import threading
import urllib.parse
from typing import Any, Callable, Optional

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from .config import get_config
from .constant import State, Url
from .log import get_logger
from .util import asyncio_run


@dataclasses.dataclass
class Status:
    date_time: datetime.datetime
    state: State


class SimpleCycuCico:
    def __init__(self, username: str, password: str):
        self.username: str = username
        self.password: str = password

        self.clean_up()

        edge_options: webdriver.EdgeOptions = webdriver.EdgeOptions()
        edge_options.add_argument(f"user-data-dir={os.getcwd()}")
        self.edge_driver: webdriver.Edge = webdriver.Edge(options=edge_options)

        self.login(username, password)

    @classmethod
    def clean_up(cls):
        def on_rm_error(func: Callable[[Any], None], path: str, exc_info: Any):
            try:
                os.chmod(path, stat.S_IWRITE)
                func(path)
            except Exception as e:
                get_logger().exception(e)

        path: str
        for path in [
            'Ad Blocking',
            'BrowserMetrics',
            'CertificateRevocation',
            'chrome_debug.log',
            'Crashpad',
            'CrashpadMetrics-active.pma',
            'CrashpadMetrics.pma',
            'Default',
            'DevToolsActivePort',
            'Edge Shopping',
            'edge_shutdown_ms.txt',
            'First Run',
            'FirstLaunchAfterInstallation',
            'Functional Data',
            'Functional Data-wal',
            'Functional SAN Data',
            'Functional SAN Data-wal',
            'GrShaderCache',
            'Last Browser',
            'Last Version',
            'Local State',
            'OriginTrials',
            'RecoveryImproved',
            'Safe Browsing',
            'ShaderCache',
            'SmartScreen',
            'Speech Recognition',
            'Subresource Filter',
            'Trust Protection Lists',
            'Web Notifications Deny List',
            'WidevineCdm',
            'ZxcvbnData',
        ]:
            if not os.path.exists(path):
                continue

            if os.path.isdir(path) and not os.path.islink(path):
                shutil.rmtree(path, onerror=on_rm_error)
            else:
                try:
                    os.chmod(path, stat.S_IWRITE)
                    os.remove(path)
                except Exception as e:
                    get_logger().exception(e)

    def login(self, username: str, password: str):
        get_logger().info(f"Logging in...")
        self.edge_driver.get(Url.BASE)

        d: webdriver.Edge
        WebDriverWait(self.edge_driver, 6).until(lambda d: d.find_element(By.NAME, 'UserNm'))
        self.edge_driver.find_element(By.NAME, 'UserNm').send_keys(username)

        WebDriverWait(self.edge_driver, 1).until(lambda d: d.find_element(By.NAME, 'UserPasswd'))
        self.edge_driver.find_element(By.NAME, 'UserPasswd').send_keys(password)
        self.edge_driver.find_element(By.NAME, 'UserPasswd').submit()

        WebDriverWait(self.edge_driver, 6).until(lambda d: d.find_element(By.ID, 'profile'))

    def get_status(self) -> Optional[Status]:
        get_logger().info("Getting the status...")
        self.edge_driver.get(urllib.parse.urljoin(Url.BASE, Url.ATTENDANCE))

        d: webdriver.Edge
        WebDriverWait(self.edge_driver, 12).until(lambda d: d.find_element(By.ID, 'logTable'))
        log: str = self.edge_driver.find_element(By.ID, 'logTable').get_attribute('innerHTML')
        last_sign_date_time: str = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}', log)[0]
        last_sign_state: str = re.search('無紙化平台簽.', log)[0]
        status: Status = Status(
            date_time=datetime.datetime.strptime(last_sign_date_time, '%Y-%m-%d %H:%M'),
            state=State.CLOCK_IN if '到' in last_sign_state else State.CLOCK_OUT)
        get_logger().info(f"Status: {status}")
        return status

    def clock(self, state: State):
        get_logger().info(f"Clocking {state}...")
        self.edge_driver.get(Url.BASE)

        d: webdriver.Edge

        if state == State.CLOCK_IN:
            WebDriverWait(self.edge_driver, 6).until(lambda d: d.find_element(By.CSS_SELECTOR, '.btn-primary'))
            self.edge_driver.find_element(By.CSS_SELECTOR, '.btn-primary').click()
        elif state == State.CLOCK_OUT:
            WebDriverWait(self.edge_driver, 6).until(lambda d: d.find_element(By.CSS_SELECTOR, '.btn-info'))
            self.edge_driver.find_element(By.CSS_SELECTOR, '.btn-info').click()

        WebDriverWait(self.edge_driver, 6).until(
            lambda d: d.find_element(By.CSS_SELECTOR, '.swal2-styled.swal2-confirm'))
        self.edge_driver.find_element(By.CSS_SELECTOR, '.swal2-styled.swal2-confirm').click()


class CycuCicoScheduler:
    def __init__(self, status: Status):
        self.status: Status = status

    def __iter__(self):
        return self

    def __next__(self) -> Status:
        next_date_time: datetime.datetime
        next_state = State.CLOCK_OUT if self.status.state == State.CLOCK_IN else State.CLOCK_IN

        now: datetime.datetime = datetime.datetime.now()
        if next_state == State.CLOCK_OUT:
            if now.day > self.status.date_time.day:
                next_date_time = datetime.datetime.now()
            elif now > datetime.datetime(
                    self.status.date_time.year, self.status.date_time.month, self.status.date_time.day,
                    get_config().clock_out_end_time.hour,
                    get_config().clock_out_end_time.minute,
                    get_config().clock_out_end_time.second):
                next_date_time = datetime.datetime.now()
            else:
                start_point: datetime = datetime.datetime(
                    now.year, now.month, now.day,
                    get_config().clock_out_start_time.hour,
                    get_config().clock_out_start_time.minute,
                    get_config().clock_out_start_time.second)
                end_point: datetime = datetime.datetime(
                    now.year, now.month, now.day,
                    get_config().clock_out_end_time.hour,
                    get_config().clock_out_end_time.minute,
                    get_config().clock_out_end_time.second)
                offset: datetime.timedelta = datetime.timedelta(
                    seconds=random.randint(0, int((end_point - start_point).total_seconds())))
                next_date_time = start_point + offset
        else:
            start_point: datetime = datetime.datetime(
                now.year, now.month, now.day,
                get_config().clock_in_start_time.hour,
                get_config().clock_in_start_time.minute,
                get_config().clock_in_start_time.second)
            end_point: datetime = datetime.datetime(
                now.year, now.month, now.day,
                get_config().clock_in_end_time.hour,
                get_config().clock_in_end_time.minute,
                get_config().clock_in_end_time.second)
            offset: datetime.timedelta = datetime.timedelta(
                seconds=random.randint(0, int((end_point - start_point).total_seconds())))
            next_date_time = start_point + offset
            while next_date_time.day < self.status.date_time.day:
                next_date_time += datetime.timedelta(days=1)
            while True:
                next_date_time += datetime.timedelta(days=1)
                if get_config().exclude_weekends and next_date_time.weekday() >= 5:
                    continue
                if get_config().exclude_specific_dates and next_date_time.date() in map(
                        datetime.date.fromisoformat, get_config().specific_dates):
                    continue
                break

        self.status = Status(date_time=next_date_time, state=next_state)
        return self.status


class CycuCicoThread(threading.Thread):
    def __init__(self, *args, daemon: bool = True, **kwargs):
        super().__init__(*args, daemon=daemon, **kwargs)

        self.loop: Optional[asyncio.BaseEventLoop] = None
        self.stop_future: Optional[asyncio.Future] = None

        self._next: Optional[Status] = None
        self._on_next_changed_listeners: list[Callable[[Optional[Status]], None]] = list()

    @property
    def next(self) -> Optional[Status]:
        return self._next

    @next.setter
    def next(self, value: Optional[Status]):
        get_logger().info(f"Next: {value}")
        self._next = value

        fn: Callable[[Optional[Status]], None]
        for fn in self._on_next_changed_listeners:
            fn(value)

    def add_on_next_changed_listener(self, listener: Callable[[Optional[Status]], None]):
        self._on_next_changed_listeners.append(listener)

    def start(self):
        super().start()

    def run(self):
        asyncio_run(self.looper())

    def stop(self):
        if self.stop_future:
            if not self.stop_future.done():
                if self.loop:
                    try:
                        self.loop.call_soon_threadsafe(self.stop_future.cancel)
                        self.stop_future = None
                    except Exception:
                        pass
        self.next = None

    async def looper(self):
        get_logger().info(f"Loop started")
        self.loop = asyncio.get_running_loop()
        self.stop_future = asyncio.get_running_loop().create_future()

        while True:
            if not self.stop_future:
                get_logger().info(f"Loop stopped")
                break

            status: Optional[Status] = None
            try:
                status = SimpleCycuCico(get_config().account, get_config().password).get_status()
            except TimeoutException as e:
                get_logger().exception(e)
            if not status:
                await asyncio.sleep(3)
                continue

            self.next = next(CycuCicoScheduler(status))

            try:
                await asyncio.wait_for(self.stop_future, (self.next.date_time - datetime.datetime.now()).total_seconds())
            except asyncio.TimeoutError:
                pass
            except asyncio.CancelledError:
                get_logger().info(f"Loop stopped")
                break
            except Exception as e:
                get_logger().info(f"Loop stopped")
                logging.exception(e)
                break

            get_logger().info(f"Doing the scheduled action...")
            for _ in range(3):
                try:
                    SimpleCycuCico(get_config().account, get_config().password).clock(self.next.state)
                    break
                except TimeoutException as e:
                    logging.exception(e)
                await asyncio.sleep(3)
