import dataclasses
import datetime
import logging
import os
import re
import shutil
import urllib.parse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from .constant import State, Url


@dataclasses.dataclass
class SignLog:
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

    def clean_up(self):
        shutil.rmtree('Ad Blocking', ignore_errors=True)
        shutil.rmtree('BrowserMetrics', ignore_errors=True)
        shutil.rmtree('Crashpad', ignore_errors=True)
        try:
            os.remove('CrashpadMetrics-active.pma')
        except Exception:
            pass
        try:
            os.remove('CrashpadMetrics.pma')
        except Exception:
            pass
        shutil.rmtree('Default', ignore_errors=True)
        try:
            os.remove('DevToolsActivePort')
        except Exception:
            pass
        try:
            os.remove('First Run')
        except Exception:
            pass
        try:
            os.remove('FirstLaunchAfterInstallation')
        except Exception:
            pass
        try:
            os.remove('Functional Data')
        except Exception:
            pass
        try:
            os.remove('Functional Data-wal')
        except Exception:
            pass
        try:
            os.remove('Functional SAN Data')
        except Exception:
            pass
        try:
            os.remove('Functional SAN Data-wal')
        except Exception:
            pass
        shutil.rmtree('GrShaderCache', ignore_errors=True)
        try:
            os.remove('Last Browser')
        except Exception:
            pass
        try:
            os.remove('Last Version')
        except Exception:
            pass
        try:
            os.remove('Local State')
        except Exception:
            pass
        shutil.rmtree('ShaderCache', ignore_errors=True)
        shutil.rmtree('SmartScreen', ignore_errors=True)
        try:
            os.remove('edge_shutdown_ms.txt')
        except Exception:
            pass

    def login(self, username: str, password: str):
        self.edge_driver.get(Url.BASE)

        d: webdriver.Edge
        WebDriverWait(self.edge_driver, 10).until(lambda d: d.find_element(By.NAME, 'UserNm'))
        self.edge_driver.find_element(By.NAME, 'UserNm').send_keys(username)
        self.edge_driver.find_element(By.NAME, 'UserPasswd').send_keys(password)
        self.edge_driver.find_element(By.NAME, 'UserPasswd').submit()

        WebDriverWait(self.edge_driver, 10).until(lambda d: d.find_element(By.ID, 'profile'))

    def get_last_sign_log(self) -> SignLog:
        self.edge_driver.get(urllib.parse.urljoin(Url.BASE, Url.ATTENDANCE))

        d: webdriver.Edge
        WebDriverWait(self.edge_driver, 10).until(lambda d: d.find_element(By.ID, 'logTable'))

        log_table:
        log: str = self.edge_driver.find_element(By.ID, 'logTable').get_attribute('innerHTML')

        last_sign_date_time: str = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}', log)[0]
        last_sign_state: str = re.search('無紙化平台簽.', log)[0]
        sign_log: SignLog = SignLog(
            date_time=datetime.datetime.strptime(last_sign_date_time, '%Y-%m-%d %H:%M'),
            state=State.CLOCK_IN if '到' in last_sign_state else State.CLOCK_OUT)
        return sign_log

    def clock(self, state: State):
        self.edge_driver.get(Url.BASE)

        d: webdriver.Edge
        WebDriverWait(self.edge_driver, 10).until(lambda d: d.find_element(By.CSS_SELECTOR, '.btn-primary'))

        if state == State.CLOCK_IN:
            self.edge_driver.find_element(By.CSS_SELECTOR, '.btn-primary').click()
        elif state == State.CLOCK_OUT:
            self.edge_driver.find_element(By.CSS_SELECTOR, '.btn-info').click()

        WebDriverWait(self.edge_driver, 10).until(
            lambda d: d.find_element(By.CSS_SELECTOR, '.swal2-styled.swal2-confirm'))

        self.edge_driver.find_element(By.CSS_SELECTOR, '.swal2-styled.swal2-confirm').click()
