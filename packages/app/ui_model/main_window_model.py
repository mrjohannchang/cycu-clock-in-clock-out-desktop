import datetime

import cycu_cico_sdk as sdk
from .ui_model import UIModel


class MainWindowModel(UIModel):
    def __init__(self):
        super().__init__()

        self._tab_bar_enabled: bool = True
        self._account_line_edit_enabled: bool = False
        self._password_line_edit_enabled: bool = False
        self._clock_in_start_time_edit_enabled: bool = False
        self._clock_in_end_time_edit_enabled: bool = False
        self._clock_out_start_time_edit_enabled: bool = False
        self._clock_out_end_time_edit_enabled: bool = False
        self._exclude_weekends_check_box_enabled: bool = False
        self._exclude_specific_dates_check_box_enabled: bool = False
        self._specific_dates_text_edit_enabled: bool = False
        self._save_push_button_enabled: bool = False
        self._cancel_push_button_enabled: bool = False
        self._edit_push_button_enabled: bool = True

        self._clock_in_push_button_enabled: bool = False
        self._clock_out_push_button_enabled: bool = False

        self._stop_push_button_enabled: bool = False
        self._start_push_button_enabled: bool = False

        self._active_tab: int = sdk.get_config().active_tab
        self._account: str = sdk.get_config().account
        self._password: str = sdk.get_config().password
        self._clock_in_start_time: datetime.time = sdk.get_config().clock_in_start_time
        self._clock_in_end_time: datetime.time = sdk.get_config().clock_in_end_time
        self._clock_out_start_time: datetime.time = sdk.get_config().clock_out_start_time
        self._clock_out_end_time: datetime.time = sdk.get_config().clock_out_end_time
        self._exclude_weekends: bool = sdk.get_config().exclude_weekends
        self._exclude_specific_dates: bool = sdk.get_config().exclude_specific_dates
        self._specific_dates: list[str] = sdk.get_config().specific_dates
        self._status: str = ''
        self._next: str = ''

    @property
    def tab_bar_enabled(self) -> bool:
        return self._tab_bar_enabled

    @tab_bar_enabled.setter
    def tab_bar_enabled(self, enabled: bool):
        self._tab_bar_enabled = enabled

    @property
    def account_line_edit_enabled(self) -> bool:
        return self._account_line_edit_enabled

    @account_line_edit_enabled.setter
    def account_line_edit_enabled(self, enabled: bool):
        self._account_line_edit_enabled = enabled

    @property
    def password_line_edit_enabled(self) -> bool:
        return self._password_line_edit_enabled

    @password_line_edit_enabled.setter
    def password_line_edit_enabled(self, enabled: bool):
        self._password_line_edit_enabled = enabled

    @property
    def clock_in_start_time_edit_enabled(self) -> bool:
        return self._clock_in_start_time_edit_enabled

    @clock_in_start_time_edit_enabled.setter
    def clock_in_start_time_edit_enabled(self, enabled: bool):
        self._clock_in_start_time_edit_enabled = enabled

    @property
    def clock_in_end_time_edit_enabled(self) -> bool:
        return self._clock_in_end_time_edit_enabled

    @clock_in_end_time_edit_enabled.setter
    def clock_in_end_time_edit_enabled(self, enabled: bool):
        self._clock_in_end_time_edit_enabled = enabled

    @property
    def clock_out_start_time_edit_enabled(self) -> bool:
        return self._clock_out_start_time_edit_enabled

    @clock_out_start_time_edit_enabled.setter
    def clock_out_start_time_edit_enabled(self, enabled: bool):
        self._clock_out_start_time_edit_enabled = enabled

    @property
    def clock_out_end_time_edit_enabled(self) -> bool:
        return self._clock_out_end_time_edit_enabled

    @clock_out_end_time_edit_enabled.setter
    def clock_out_end_time_edit_enabled(self, enabled: bool):
        self._clock_out_end_time_edit_enabled = enabled

    @property
    def exclude_weekends_check_box_enabled(self) -> bool:
        return self._exclude_weekends_check_box_enabled

    @exclude_weekends_check_box_enabled.setter
    def exclude_weekends_check_box_enabled(self, enabled: bool):
        self._exclude_weekends_check_box_enabled = enabled

    @property
    def exclude_specific_dates_check_box_enabled(self) -> bool:
        return self._exclude_specific_dates_check_box_enabled

    @exclude_specific_dates_check_box_enabled.setter
    def exclude_specific_dates_check_box_enabled(self, enabled: bool):
        self._exclude_specific_dates_check_box_enabled = enabled

    @property
    def specific_dates_text_edit_enabled(self) -> bool:
        return self._specific_dates_text_edit_enabled

    @specific_dates_text_edit_enabled.setter
    def specific_dates_text_edit_enabled(self, enabled: bool):
        self._specific_dates_text_edit_enabled = enabled

    @property
    def save_push_button_enabled(self) -> bool:
        return self._save_push_button_enabled

    @save_push_button_enabled.setter
    def save_push_button_enabled(self, enabled: bool):
        self._save_push_button_enabled = enabled

    @property
    def cancel_push_button_enabled(self) -> bool:
        return self._cancel_push_button_enabled

    @cancel_push_button_enabled.setter
    def cancel_push_button_enabled(self, enabled: bool):
        self._cancel_push_button_enabled = enabled

    @property
    def edit_push_button_enabled(self) -> bool:
        return self._edit_push_button_enabled

    @edit_push_button_enabled.setter
    def edit_push_button_enabled(self, enabled: bool):
        self._edit_push_button_enabled = enabled

    @property
    def clock_in_push_button_enabled(self) -> bool:
        return self._clock_in_push_button_enabled

    @clock_in_push_button_enabled.setter
    def clock_in_push_button_enabled(self, enabled: bool):
        self._clock_in_push_button_enabled = enabled

    @property
    def clock_out_push_button_enabled(self) -> bool:
        return self._clock_out_push_button_enabled

    @clock_out_push_button_enabled.setter
    def clock_out_push_button_enabled(self, enabled: bool):
        self._clock_out_push_button_enabled = enabled

    @property
    def stop_push_button_enabled(self) -> bool:
        return self._stop_push_button_enabled

    @stop_push_button_enabled.setter
    def stop_push_button_enabled(self, enabled: bool):
        self._stop_push_button_enabled = enabled

    @property
    def start_push_button_enabled(self) -> bool:
        return self._start_push_button_enabled

    @start_push_button_enabled.setter
    def start_push_button_enabled(self, enabled: bool):
        self._start_push_button_enabled = enabled

    @property
    def active_tab(self) -> int:
        return self._active_tab

    @active_tab.setter
    def active_tab(self, value: int):
        self._active_tab = value

    @property
    def account(self) -> str:
        return self._account

    @account.setter
    def account(self, value: str):
        self._account = value

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, value: str):
        self._password = value

    @property
    def clock_in_start_time(self) -> datetime.time:
        return self._clock_in_start_time

    @clock_in_start_time.setter
    def clock_in_start_time(self, value: datetime.time):
        self._clock_in_start_time = value

    @property
    def clock_in_end_time(self) -> datetime.time:
        return self._clock_in_end_time

    @clock_in_end_time.setter
    def clock_in_end_time(self, value: datetime.time):
        self._clock_in_end_time = value

    @property
    def clock_out_start_time(self) -> datetime.time:
        return self._clock_out_start_time

    @clock_out_start_time.setter
    def clock_out_start_time(self, value: datetime.time):
        self._clock_out_start_time = value

    @property
    def clock_out_end_time(self) -> datetime.time:
        return self._clock_out_end_time

    @clock_out_end_time.setter
    def clock_out_end_time(self, value: datetime.time):
        self._clock_out_end_time = value

    @property
    def exclude_weekends(self) -> bool:
        return self._exclude_weekends

    @exclude_weekends.setter
    def exclude_weekends(self, value: bool):
        self._exclude_weekends = value

    @property
    def exclude_specific_dates(self) -> bool:
        return self._exclude_specific_dates

    @exclude_specific_dates.setter
    def exclude_specific_dates(self, value: bool):
        self._exclude_specific_dates = value

    @property
    def specific_dates(self) -> list[str]:
        return self._specific_dates

    @specific_dates.setter
    def specific_dates(self, value: list[str]):
        self._specific_dates = value

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        self._status = value

    @property
    def next(self) -> str:
        return self._next

    @next.setter
    def next(self, value: str):
        self._next = value

    def save(self):
        self.tab_bar_enabled = True
        self.account_line_edit_enabled = False
        self.password_line_edit_enabled = False
        self.clock_in_start_time_edit_enabled = False
        self.clock_in_end_time_edit_enabled = False
        self.clock_out_start_time_edit_enabled = False
        self.clock_out_end_time_edit_enabled = False
        self.exclude_weekends_check_box_enabled = False
        self.exclude_specific_dates_check_box_enabled = False
        self.specific_dates_text_edit_enabled = False
        self.save_push_button_enabled = False
        self.cancel_push_button_enabled = False
        self.edit_push_button_enabled = True

        sdk.get_config().account = self._account
        sdk.get_config().password = self._password
        sdk.get_config().clock_in_start_time = self._clock_in_start_time
        sdk.get_config().clock_in_end_time = self._clock_in_end_time
        sdk.get_config().clock_out_start_time = self._clock_out_start_time
        sdk.get_config().clock_out_end_time = self._clock_out_end_time
        sdk.get_config().exclude_weekends = self._exclude_weekends
        sdk.get_config().exclude_specific_dates = self._exclude_specific_dates
        sdk.get_config().specific_dates = self._specific_dates
        sdk.save_config()

    def cancel(self):
        self.tab_bar_enabled = True
        self.account_line_edit_enabled = False
        self.password_line_edit_enabled = False
        self.clock_in_start_time_edit_enabled = False
        self.clock_in_end_time_edit_enabled = False
        self.clock_out_start_time_edit_enabled = False
        self.clock_out_end_time_edit_enabled = False
        self.exclude_weekends_check_box_enabled = False
        self.exclude_specific_dates_check_box_enabled = False
        self.specific_dates_text_edit_enabled = False
        self.save_push_button_enabled = False
        self.cancel_push_button_enabled = False
        self.edit_push_button_enabled = True

        self.account = sdk.get_config().account
        self.password = sdk.get_config().password
        self.clock_in_start_time = sdk.get_config().clock_in_start_time
        self.clock_in_end_time = sdk.get_config().clock_in_end_time
        self.clock_out_start_time = sdk.get_config().clock_out_start_time
        self.clock_out_end_time = sdk.get_config().clock_out_end_time
        self.exclude_weekends = sdk.get_config().exclude_weekends
        self.exclude_specific_dates = sdk.get_config().exclude_specific_dates
        self.specific_dates = sdk.get_config().specific_dates

    def edit(self):
        self.tab_bar_enabled = False
        self.edit_push_button_enabled = False
        self.account_line_edit_enabled = True
        self.password_line_edit_enabled = True
        self.clock_in_start_time_edit_enabled = True
        self.clock_in_end_time_edit_enabled = True
        self.clock_out_start_time_edit_enabled = True
        self.clock_out_end_time_edit_enabled = True
        self.exclude_weekends_check_box_enabled = True
        self.exclude_specific_dates_check_box_enabled = True
        self.specific_dates_text_edit_enabled = True
        self.save_push_button_enabled = True
        self.cancel_push_button_enabled = True

    def update_status(self):
        sign_log: sdk.SignLog = sdk.SimpleCycuCico(sdk.get_config().account, sdk.get_config().password) \
            .get_last_sign_log()
        self.status = f"Status: Clocked {'in' if sign_log.state == sdk.State.CLOCK_IN else 'out'}" \
                      f" at {sign_log.date_time.time().isoformat()} on {sign_log.date_time.date().isoformat()}"

    def clock_in(self):
        pass

    def clock_out(self):
        pass

    def stop(self):
        pass

    def start(self):
        pass
