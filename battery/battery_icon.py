import time
import datetime

import gobject

from rox import processes

from traylib.menu_icon import MenuIcon


class BatteryIcon(MenuIcon):

    def __init__(self, tray, icon_config, tray_config, battery):
        MenuIcon.__init__(self, tray, icon_config, tray_config)
        self.__battery = battery
        self.__update()
        self.__check_low()

        gobject.timeout_add(5000, self.__update)
        gobject.timeout_add(120000, self.__check_low)

    def __warn_low(self):
        processes.PipeThroughCommand([
            "notify-send", "--icon=%s" % self.find_icon_name(),
            _("Battery is low!")
        ], None, None).start()

    def __check_low(self):
        t = time.strptime(self.__battery.time, '%H:%M:%S')
        d = datetime.timedelta(0, t.tm_sec, 0, 0, t.tm_min, t.tm_hour)
        seconds = d.total_seconds()
        if seconds <= 5 * 60:
            self.__warn_low()
        return True

    def __update(self):
        self.__battery.update()
        self.update_icon()
        self.update_tooltip()
        return True

    def get_icon_names(self):
        percent = self.__battery.percent
        if self.__battery.missing:
            return ['battery-missing']
        if self.__battery.charging:
            if percent <= 10:
                return ['battery-caution-charging']
            if percent <= 30:
                return ['battery-low-charging']
            if percent <= 75:
                return ['battery-good-charging']
            elif percent <= 95:
                return ['battery-full-charging']
            else:
                return ['battery-full-charged']
        else:
            if percent == 0:
                return ['battery-empty']
            if percent <= 10:
                return ['battery-caution']
            if percent <= 30:
                return ['battery-low']
            if percent <= 75:
                return ['battery-good']
            else:
                return ['battery-full']

    def make_tooltip(self):
        if self.__battery.missing:
            return _('No battery')
        return '%s %% (%s %s)' % (
            self.__battery.percent,
            self.__battery.time,
            _('until charged') if self.__battery.charging else _('remaining')
        )
