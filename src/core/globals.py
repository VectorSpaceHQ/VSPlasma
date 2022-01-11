# -*- coding: utf-8 -*-
import os
from pathlib import Path

home = str(Path.home())
FITTING_TOLERANCE = 0.001
SPLINE_CHECK = 3
VERSION = ''
DATE = ''
open_path = '../tests/'
point_tolerance = 0.001
folder = None
DEFAULT_CONFIG_DIR = os.path.join(home + '/.config/vsplasma')

class Globals():
    def __init__():
        self.FITTING_TOLERANCE = 0.001
        self.SPLINE_CHECK = 3
        self.VERSION = ''
        self.DATE = ''
        self.open_path = '../tests/'
        self.point_tolerance = 0.001

    def read_user_config():
        pass
