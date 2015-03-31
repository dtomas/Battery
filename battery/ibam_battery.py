import re
import subprocess


PERCENT_RE = re.compile(r'Battery percentage: +(?P<percent>[0-9]+) %')
TIME_RE = re.compile(r'Battery time left: +(?P<time>[0-9]+:[0-9]+:[0-9]+)')


class Battery(object):

    def __init__(self):
        self.percent = 0
        self.time = ''
        self.charging = False
        self.update()

    def update(self):
        p = subprocess.Popen(
            ['ibam', '--percentbattery', '--battery'], stdout=subprocess.PIPE
        )
        out_data, err_data = p.communicate()
        for line in out_data.split('\n'):
            m = PERCENT_RE.match(line)
            if m is not None:
                self.percent = m.groupdict()['percent']
            m = TIME_RE.match(line)
            if m is not None:
                self.time = m.groupdict()['time']
