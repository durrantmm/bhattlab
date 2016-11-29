import os

from ..shared.log import Log
from ..shared.state_superclass import *

class MergeState(StateSuperClass):
    def __init__(self, args):
        StateSuperClass.__init__(self)

        self.which = 'merge'

        self.paths = Paths(ispeaks_dirs=args['ispeaks_directories'],
                           output_dir=args['output_dir'])

        self.settings = Settings()

        self.logger = Log(self.paths.out_dir)

class Paths(PathsSuperClass):
    def __init__(self, ispeaks_dirs, output_dir):
        PathsSuperClass.__init__(self, output_dir)
        # Directories
        self.ispeaks_dirs = [self.makedir(dir) for dir in ispeaks_dirs]
        self.sam_info = None

    def makedir(self, path):
        if not os.path.isdir(path):
            os.makedirs(path)
        return os.path.abspath(path)


class Settings(SettingsSuperClass):
    def __init__(self):
        SettingsSuperClass.__init__(self)