from functools import partial

import rox
from rox.options import Option

from traylib import ICON_THEME
from traylib.main import Main
from traylib.tray import Tray

from battery.acpi_battery import Battery
from battery.battery_icon import BatteryIcon


class BatteryMain(Main):
    
    def __init__(self):
        Main.__init__(self, "Battery")

    def init_options(self):
        Main.init_options(self)
        
    def init_config(self):
        Main.init_config(self)
        
    def mainloop(self, app_args):
        Main.mainloop(
            self, app_args,
            partial(Tray, create_menu_icon=partial(
                BatteryIcon, battery=Battery()
            ))
        )

    def options_changed(self):
        Main.options_changed(self)
