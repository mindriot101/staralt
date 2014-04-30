class InsufficientParameters(RuntimeError): pass

class StarAlt(object):
    DEFAULT_MOON_DISTANCE = True
    DEFAULT_MIN_ELEVATION = 30

    REQUIRED_PARAMS = ['mode', 'date', 'coordinates',
            'moon_distance', 'min_elevation']

    def __init__(self):
        self.moon_distance = self.DEFAULT_MOON_DISTANCE
        self.min_elevation = self.DEFAULT_MIN_ELEVATION
        self.mode = None
        self.date = None
        self.coordinates = []

    def save_image(self, filename):
        if self.insufficient_parameters():
            raise InsufficientParameters

    def insufficient_parameters(self):
        return all(getattr(self, param) is not None
                for param in self.REQUIRED_PARAMS)
