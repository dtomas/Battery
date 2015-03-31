import re
import subprocess


ACPI_RE = re.compile(
    r'Battery [0-9]+: (?P<dis>Dis)?[cC]harging, (?P<percent>[0-9]+)%, '
    r'(?P<time>[0-9]+:[0-9]+:[0-9]+)'
)


class Battery(object):

    def __init__(self):
        self.percent = 0
        self.time = ''
        self.charging = False
        self.update()

    def update(self):
        p = subprocess.Popen(['acpi'], stdout=subprocess.PIPE)
        out_data, err_data = p.communicate()
        m = ACPI_RE.match(out_data)
        if m is None:
            return
        d = m.groupdict()
        self.percent = int(d['percent'])
        self.time = d['time']
        self.charging = not bool(d['dis'])
