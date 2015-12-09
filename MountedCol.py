class MountedCollection:
    def __init__(self):
        self.mountedArchers={}
        self.last_key=0

    def addMountedArcher(self, mountedArcher):
        self.last_key += 1
        self.mountedArchers[self.last_key] = mountedArcher

    def getMountedArcher(self, key):
        return self.mountedArchers[key]

    def getMountedArchers(self):
        return sorted(self.mountedArchers.items())