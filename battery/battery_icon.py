import gobject

from traylib.menu_icon import MenuIcon


class BatteryIcon(MenuIcon):

    def __init__(self, tray, icon_config, tray_config, battery):
        MenuIcon.__init__(self, tray, icon_config, tray_config)
        self.__battery = battery

        gobject.timeout_add(5000, self.__update)

    def __update(self):
        self.__battery.update()
        self.update_icon()
        self.update_tooltip()
        return True

    def get_icon_names(self):
        percent = self.__battery.percent
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
        return '%s %% (%s %s)' % (
            self.__battery.percent,
            self.__battery.time,
            _('until charged') if self.__battery.charging else _('remaining')
        )
