import re
import subprocess


try:
    subprocess.Popen(['acpi'])
except OSError:
    raise ImportError("Command 'acpi' was not found.")


ACPI_RE = re.compile(
    r'Battery [0-9]+: ((?P<dis>Dis)?[cC]harging)?(?P<full>Full)?'
    ', (?P<percent>[0-9]+)%(, (?P<time>[0-9]+:[0-9]+:[0-9]+))?'
)


class Battery(object):

    def __init__(self):
        self.percent = 0
        self.time = ''
        self.state = ''
        self.update()

    def update(self):
        p = subprocess.Popen(['acpi'], stdout=subprocess.PIPE)
        out_data, err_data = p.communicate()
        if not out_data:
            self.state == 'MISSING'
        m = ACPI_RE.match(out_data)
        if m is None:
            return
        d = m.groupdict()
        self.percent = int(d['percent'])
        self.time = d['time']
        self.state = (
            'DISCHARGING' if d['dis'] else
            'FULL' if d['full'] else
            'CHARGING'
        )
