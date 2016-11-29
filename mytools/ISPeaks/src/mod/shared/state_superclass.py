class StateSuperClass:
    def __init__(self):
        pass

class PathsSuperClass:
    def __init__(self, outdir):
        self.out_dir = self.makedir(outdir)


class SettingsSuperClass:
    def __init__(self):
        pass

    def set_nodes(self):
        pass

    def set_names(self):
        pass

    def set_ranks(self):
        pass

